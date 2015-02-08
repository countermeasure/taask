from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',

    url(r'^$', 'tasks.views.home'),
    url(r'^(view|project)/(\w+)/tasks/$', 'tasks.views.list_tasks',
        name='list-tasks'),
    url(r'^task/add/$', 'tasks.views.add_task', name='add-task'),
    url(r'^task/edit/(\d{1,6})/$', 'tasks.views.edit_task', name='edit-task'),
    url(r'^task/postpone/(\d{1,6})/(\d{1,6})/$', 'tasks.views.postpone_task',
        name='postpone-task'),
    url(r'^task/complete/(\d{1,6})/$', 'tasks.views.complete_task',
        name='complete-task'),
    url(r'^task/rubbish/empty/$', 'tasks.views.empty_rubbish',
        name='empty-rubbish'),
    url(r'^task/rubbish/(\d{1,6})/$', 'tasks.views.rubbish_task',
        name='rubbish-task'),
    url(r'^(context|priority|project)/list/$', 'tasks.views.attribute_list',
        name='attribute-list'),
    url(r'^(context|priority|project)/add/$', 'tasks.views.attribute_add_edit',
        name='attribute-add'),
    url(r'^(context|priority|project)/edit/(\d{1,6})$',
        'tasks.views.attribute_add_edit',
        name='attribute-edit'),
    url(r'^(context|priority|project)/delete/(\d{1,6})$',
        'tasks.views.attribute_delete',
        name='attribute-delete'),
    url(r'^documentation/$', 'tasks.views.documentation', name='documentation'),
)

if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )
