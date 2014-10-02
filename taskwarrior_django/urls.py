from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'taskwarrior_django.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^add-task$', 'tasks.views.add_task', name='add-task'),
    url(r'^list-tasks$', 'tasks.views.list_tasks',
        name='list-tasks'),
    url(r'^edit-task/(\d{1,6})/$', 'tasks.views.edit_task', name='edit-task'),
)
