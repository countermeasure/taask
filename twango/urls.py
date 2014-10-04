from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'twango.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^add-task/', 'tasks.views.add_task', name='add-task'),
    url(r'^list-tasks/(\w+)/', 'tasks.views.list_tasks', name='list-tasks'),
    url(r'^edit-task/(\d{1,6})/', 'tasks.views.edit_task', name='edit-task'),
    url(r'^delete-task/(\d{1,6})/', 'tasks.views.delete_task',
        name='delete-task'),
    url(r'^configuration/', 'tasks.views.configuration', name='configuration'),
    url(r'^documentation/', 'tasks.views.documentation', name='documentation'),
)
