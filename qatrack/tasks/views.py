from django.views.generic import FormView, ListView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import HttpResponseRedirect
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.forms.models import model_to_dict

from qatrack.tasks.forms import AddOrEditTaskForm, PerformTaskForm
from qatrack.tasks.models import Task


class AddTask(FormView):
    template_name = "tasks/add_or_edit_tasks.html"
    form_class = AddOrEditTaskForm
    success_url = reverse_lazy('tasks_overview')

    def __init__(self):
        self.can_edit = True
        self.can_perform = True
        self.can_view = True
        super(AddTask, self).__init__()

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.info(
            self.request,
            _("Your task has not been saved.")
        )
        return super(AddTask, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(AddTask, self).get_context_data(**kwargs)
        context["can_edit"] = self.can_edit
        context["can_perform"] = self.can_perform
        return context


class EditPerformOrViewTask(AddTask):
    def form_valid(self, form):
        pk = self.kwargs['pk']
        task = Task.objects.get(pk=pk)
        if self.can_edit:
            form = AddOrEditTaskForm(self.request.POST, instance=task)
        else:
            form = PerformTaskForm(self.request.POST, instance=task)
        return super(EditPerformOrViewTask, self).form_valid(form)

    def form_invalid(self, form):
        pk = self.kwargs['pk']
        task = Task.objects.get(pk=pk)
        if self.can_edit:
            form = AddOrEditTaskForm(self.request.POST, instance=task)
        else:
            form = PerformTaskForm(self.request.POST, instance=task)
        return super(EditPerformOrViewTask, self).form_invalid(form)

    def get_form(self, form_class):
        pk = self.kwargs['pk']
        user = self.request.user
        task = Task.objects.get(pk=pk)
        if task.can_edit(user):
            task_dict = model_to_dict(task)
            form_class = form_class(task_dict, instance=task)
        elif task.can_perform(user):
            task_dict = {'comment_for_reviewer': task.comment_for_reviewer, 'status': task.status}
            form_class = PerformTaskForm
            form_class = form_class(task_dict, instance=task)
        else:
            form_class = None

        self.can_edit = task.can_edit(user)
        self.can_perform = task.can_perform(user)
        return form_class

    def get_context_data(self, **kwargs):
        context = super(EditPerformOrViewTask, self).get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context["task"] = Task.objects.get(pk=pk)
        return context


class MyTasks(ListView):
    context_object_name = 'perform_tasks'
    template_name = "tasks/my_tasks.html"

    def get_queryset(self):
        excludestatuses = ['Reviewed', 'Done']
        return Task.objects.tasks_to_perform(self.request.user).exclude(status__in=excludestatuses)

    def get_context_data(self, **kwargs):
        context = super(MyTasks, self).get_context_data(**kwargs)
        excludestatuses = ['Reviewed', 'Not done']
        context['review_tasks'] = Task.objects.tasks_to_review(self.request.user).exclude(status__in=excludestatuses)
        return context


class TaskOverview(ListView):
    context_object_name = 'Tasks'
    queryset = Task.objects.exclude(status='Reviewed')
    template_name = "tasks/task_overview.html"