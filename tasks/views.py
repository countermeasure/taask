from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from tasks.forms import AddTaskForm

from taskw import TaskWarrior


w = TaskWarrior(marshal=True)
# w = TaskWarrior(config_filename="~/some_project/.taskrc")


def add_task(request):
    """Add a task."""
    if request.method == "POST":
        form = AddTaskForm(request.POST, label_suffix='')
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
            # Add the necessary UDAs in here later
            w.task_add(description, project=project, priority=priority,
                       due=due, recur=recur, until=until, wait=wait,
                       scheduled=scheduled, depends=depends)
            return HttpResponseRedirect(reverse('list-tasks'))
    else:
        form = AddTaskForm()

    return render(request, 'add_task.html', {
                           'form': form,
                           })


def list_tasks(request):

    tasks = w.load_tasks()
    list = tasks['pending']
    return render(request, 'list_tasks.html', {
                           'list': list,
                           })
