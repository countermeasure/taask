from datetime import (
    date,
    datetime,
    timedelta,
)

from django.db.models import Sum
from django.shortcuts import render, redirect

from rest_framework import generics

from forms import (
    ContextForm,
    PriorityForm,
    ProjectForm,
    TaskForm,
)
from models import (
    Context,
    Priority,
    Project,
    Task,
)
from serializers import TaskSerializer
from utils import (
    get_task_count,
    process_and_save_task,
)


def home(request):
    "Redirects requests to the root domain to the 'Today' view."""

    return redirect('list-tasks', 'view', 'today')


class TaskList(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


def complete_task(request, task_id):
    """Completes a task."""

    # TODO: Display an error if the task cannot be completed
    task = Task.objects.get(pk=task_id)
    # Only tasks from certain views are able to be completed
    if task.view in ['inbox', 'today', 'next', 'someday']:
        task.completed = datetime.now()
        task.view = 'completed'
        # Remove unnecessary data
        task.scheduled = None
        task.priority = None
        task.underway = False
        if not task.time_remaining:
            task.time_remaining = 0
        if not task.time_spent:
            task.time_spent = 0
        task.time_spent += task.time_remaining
        task.time_remaining = None
        task.save()

    return redirect('list-tasks', 'view', 'completed')


def postpone_task(request, task_id, days_to_postpone):
    """Postpones a task by the given number of days."""

    task = Task.objects.get(pk=task_id)
    referring_view = task.view
    # TODO: Add a check that task.time_remaining > 0
    # TODO: Add a check that task.deadline is after the date that the task
    # is being postponed until

    if task.view in ('today', 'scheduled'):
        days_to_postpone = int(days_to_postpone)
        task.view = 'scheduled'
        task.underway = False
        if task.scheduled:
            task.scheduled += timedelta(days=days_to_postpone)
        else:
            task.scheduled = date.today() + timedelta(days=days_to_postpone)
        task.save()

    return redirect('list-tasks', 'view', referring_view)


def rubbish_task(request, task_id):
    """Moves a task to the rubbish view."""

    task = Task.objects.get(pk=task_id)
    task.view = 'rubbish'
    task.save()

    return redirect('list-tasks', 'view', 'rubbish')


def empty_rubbish(request):
    """Empties the rubbish."""

    tasks = Task.objects.filter(view='rubbish')
    for task in tasks:
      task.delete()

    return redirect('list-tasks', 'view', 'rubbish')


def documentation(request):
    """Shows documentation."""

    return render(request, 'documentation.html', {
        'contexts': Context.objects.all(),
        'projects': Project.objects.all(),
        'task_count': get_task_count(),
    })


def attribute_add_edit(request, attribute_type=None, attribute_id=None):
    """Adds or edits the specified attribute."""

    if attribute_id:
        mode = 'edit'
        title = 'Edit %s' % attribute_type
        if attribute_type == 'context':
            current_name = context = Context.objects.get(pk=attribute_id)
        elif attribute_type == 'priority':
            current_name = priority = Priority.objects.get(pk=attribute_id)
        elif attribute_type == 'project':
            current_name = project = Project.objects.get(pk=attribute_id)
    else:
        mode = 'add'
        title = 'Add a %s' % attribute_type
        current_name = None

    if request.method == "POST":
        if attribute_id:
            if attribute_type == 'context':
                form = ContextForm(request.POST, instance=context)
            elif attribute_type == 'priority':
                form = PriorityForm(request.POST, instance=priority)
            elif attribute_type == 'project':
                form = ProjectForm(request.POST, instance=project)
        else:
            if attribute_type == 'context':
                form = ContextForm(request.POST)
            elif attribute_type == 'priority':
                form = PriorityForm(request.POST)
            elif attribute_type == 'project':
                form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('attribute-list', attribute_type)
    else:
        if attribute_id:
            if attribute_type == 'context':
                form = ContextForm(instance=context)
            elif attribute_type == 'priority':
                form = PriorityForm(instance=priority)
            elif attribute_type == 'project':
                form = ProjectForm(instance=project)
        else:
            if attribute_type == 'context':
                form = ContextForm()
            elif attribute_type == 'priority':
                form = PriorityForm()
            elif attribute_type == 'project':
                form = ProjectForm()

    return render(
        request,
        'add_edit_attribute.html',
        {
            'attribute_type': attribute_type,
            'contexts': Context.objects.all(),
            'current_name': current_name,
            'form': form,
            'mode': mode,
            'projects': Project.objects.all(),
            'task_count': get_task_count(),
            'title': title,
        },
    )


def attribute_list(request, attribute_type):
    """Shows the list of the specified type of attribute."""

    if attribute_type == 'context':
        attributes = Context.objects.all()
    elif attribute_type == 'priority':
        attributes = Priority.objects.all()
    elif attribute_type == 'project':
        attributes = Project.objects.all()

    return render(request, 'list_attributes.html', {
        'attribute_type': attribute_type,
        'attributes': attributes,
        'contexts': Context.objects.all(),
        'projects': Project.objects.all(),
        'task_count': get_task_count(),
    })


def attribute_delete(request, attribute_type, attribute_id):
    """Deletes the specified attribute if it is not attached
    to any tasks.

    Shows a notification message and does not delete the
    attribute if it is attached to any tasks.
    """

    if attribute_type == 'context':
        attribute = Context.objects.get(pk=attribute_id)
    elif attribute_type == 'priority':
        attribute = Priority.objects.get(pk=attribute_id)
    elif attribute_type == 'project':
        attribute = Project.objects.get(pk=attribute_id)

    if request.method == 'POST':
        # The template shouldn't allow a POST request if
        # there are any tasks with this attribute, but
        # test again just to be sure before deleting
        if not attribute.task_set.all().exists():
            attribute.delete()
            return redirect('attribute-list', attribute_type)

    if attribute.task_set.all().exists():
        mode = 'notify'
    else:
        mode = 'delete'

    return render(request, 'delete_attribute.html', {
        'attribute': attribute,
        'attribute_type': attribute_type,
        'contexts': Context.objects.all(),
        'mode': mode,
        'projects': Project.objects.all(),
        'task_count': get_task_count(),
    })
