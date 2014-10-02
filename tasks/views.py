from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from tasks.forms import TaskForm

from taskw import TaskWarrior


w = TaskWarrior(marshal=True)
# w = TaskWarrior(config_filename="~/some_project/.taskrc")


def add_task(request):
    """Add a task."""
    if request.method == "POST":
        form = TaskForm(request.POST, label_suffix='')
        if form.is_valid():
            description = form.cleaned_data['description']
            project = form.cleaned_data['project']
            priority = form.cleaned_data['priority']
            due = form.cleaned_data['due']
            recur = form.cleaned_data['recur']
            until = form.cleaned_data['until']
            wait = form.cleaned_data['wait']
            scheduled = form.cleaned_data['scheduled']
            depends = form.cleaned_data['depends']
            annotations = form.cleaned_data['annotations']
            tags = form.cleaned_data['tags']
            w.task_add(description, project=project, priority=priority,
                       due=due, recur=recur, until=until, wait=wait,
                       scheduled=scheduled, depends=depends,
                       annotations=annotations, tags=tags)
            return HttpResponseRedirect(reverse('list-tasks'))
    else:
        form = TaskForm()

    return render(request, 'add_task.html', {
                           'form': form,
                           })


def list_tasks(request):
    """Lists all pending tasks."""
    tasks = w.load_tasks()
    task_list = tasks['pending']
    return render(request, 'list_tasks.html', {
                           'task_list': task_list,
                           })


def edit_task(request, task_id):
    """Opens a task for viewing or editing."""

    task = w.get_task(id=task_id)

    if request.method == "POST":
        form = TaskForm(request.POST, label_suffix='')
        if form.is_valid():
            # Add the necessary UDAs into attributes later
            attributes = ['description', 'project', 'priority', 'due', 'recur',
                          'until', 'wait', 'scheduled', 'depends',
                          'annotations', 'tags']
            for attribute in attributes:
                a = form.cleaned_data[attribute]
                # if a and (task[1][attribute] != a):
                task[1][attribute] = a
            # The task_update function only accepts a task object's dictionary,
            # which is the second object in the task's tuple.
            w.task_update(task[1])
            return HttpResponseRedirect(reverse('list-tasks'))
    else:
        form = TaskForm(task[1])

    return render(request, 'edit_task.html', {
                           'task_id': task_id,
                           'form': form,
                           })


def delete_task(request, task_id):
    """Deletes a task."""

    w.task_delete(id=task_id)
    return HttpResponseRedirect(reverse('list-tasks'))


def documentation(request):
    """Shows documentation."""

    return render(request, 'documentation.html')


def configuration(request):
    """Shows configuration page."""

    return render(request, 'configuration.html')
