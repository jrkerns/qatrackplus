from django.conf.urls import patterns, url

from views import AddTask, MyTasks, TaskOverview, EditPerformOrViewTask

urlpatterns = patterns('',
    url(r'^add/$', AddTask.as_view(), name="tasks_add_task"),
    url(r'^edit/(?P<pk>\d+)/$', EditPerformOrViewTask.as_view(), name="tasks_edit_task"),
    url(r'^mytasks/$', MyTasks.as_view(), name="tasks_my_tasks"),
    url(r'^overview/$', TaskOverview.as_view(), name="tasks_overview"),
)