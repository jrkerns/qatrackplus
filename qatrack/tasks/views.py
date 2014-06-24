from django.views.generic import FormView, ListView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import HttpResponseRedirect
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.forms.models import model_to_dict

import datatableview
from datatableview.views import DatatableView, XEditableDatatableView
from datatableview.utils import get_datatable_structure
from datatableview import helpers


from qatrack.tasks.forms import TaskForm
from qatrack.tasks.models import Task


class AddTask(FormView):
    template_name = "tasks/add_or_edit_tasks.html"
    form_class = TaskForm
    success_url = reverse_lazy('tasks_add_task')

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


class EditTask(AddTask):
    def form_valid(self, form):
        pk = self.kwargs['pk']
        task = Task.objects.get(pk=pk)
        task_dict = model_to_dict(task)
        form = TaskForm(self.request.POST, instance=task)
        return super(EditTask, self).form_valid(form)

    def form_invalid(self, form):
        pk = self.kwargs['pk']
        task = Task.objects.get(pk=pk)
        form = TaskForm(data=self.request.POST, instance=task)
        return super(EditTask, self).form_invalid(form)

    def get_form(self, form_class):
        pk = self.kwargs['pk']
        user = self.request.user
        task = Task.objects.get(pk=pk)
        task_dict = model_to_dict(task)
        form_class = form_class(task_dict, instance=task)

        # Check if a user can can edit or perform a task
        self.can_edit = task.can_edit(user)
        self.can_perform = task.can_perform(user)

        return form_class


class MyTasks(ListView):
    pass


class TaskOverview(ListView):
    context_object_name = 'Tasks'
    queryset = Task.objects.exclude(status='reviewed')
    template_name = "tasks/task_overview.html"