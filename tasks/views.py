from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from tasks.forms import AddTaskForm, EditTaskForm
from taskw import TaskWarrior


w = TaskWarrior(marshal=True)
# w = TaskWarrior(config_filename="/path/to/.taskrc")


def add_task(request):
    """Add a task."""

    if request.method == "POST":
        form = AddTaskForm(request.POST, label_suffix='')
        if form.is_valid():
            # Assign each cleaned data item to its own variable
            description = form.cleaned_data['description']
            tag_view = form.cleaned_data['tag_view']
            priority = form.cleaned_data['priority']
            tag_time = form.cleaned_data['tag_time']
            project = form.cleaned_data['project']
            due = form.cleaned_data['due']
            recur = form.cleaned_data['recur']
            until = form.cleaned_data['until']
            wait = form.cleaned_data['wait']
            # Construct 'tags' in the format which taskw expects
            # tags[1] is an empty string as it's a placeholder for tag_order
            tags = [tag_view, '', tag_time]
            # Create the new task
            w.task_add(description,
                       priority=priority,
                       project=project,
                       due=due,
                       recur=recur,
                       until=until,
                       wait=wait,
                       tags=tags)
            return HttpResponseRedirect(reverse('list-tasks', args=['inbox']))
    else:
        form = AddTaskForm()

    return render(request, 'add_task.html', {
                           'form': form,
                           })


def list_tasks(request, view):
    """Shows a filtered list of tasks.

       filter_tasks() returns a list which contains one dictionary per task."""

    if view in ['inbox', 'today', 'next', 'rubbish']:
        task_list = w.filter_tasks({'status': 'pending',
                                    'tags.contains': view,})

    elif view == 'scheduled':
        task_list = w.filter_tasks({'status': 'waiting',})

    elif view == 'completed':
        task_list = w.filter_tasks({'status': 'completed',})

    return render(request, 'list_tasks.html', {
                           'task_list': task_list,
                           'view': view,
                           })


def edit_task(request, task_id):
    """Opens a task for viewing or editing."""

    id, task = w.get_task(id=task_id)

    if request.method == "POST":
        form = EditTaskForm(request.POST, label_suffix='')
        if form.is_valid():
            # Write non-tag attributes to the task
            non_tag_fields = ['description',
                              'priority',
                              'project',
                              'due',
                              'recur',
                              'until',
                              'wait']
            for attribute in non_tag_fields:
                value = form.cleaned_data[attribute]
                task[attribute] = value
            # Create the tag attribute in the format which taskw expects and
            # write it to the task
            tag_fields = ['tag_view',
                          'tag_order',
                          'tag_time']
            tags = []
            for attribute in tag_fields:
                value = form.cleaned_data[attribute]
                tags.append(value)
            task['tags'] = tags
            # Update the task
            w.task_update(task)
            return HttpResponseRedirect(reverse('list-tasks', args=['inbox']))
    else:
        # Add each individual tag item to the task object so that they are
        # displayed in the form
        tags = task['tags']
        task['tag_view'] = tags[0]
        task['tag_order'] = tags[1]
        task['tag_time'] = tags[2]
        # Instantiate the form with the task dictionary containing the seperate
        # tags
        form = EditTaskForm(task)

    return render(request, 'edit_task.html', {
                           'task_id': task_id,
                           'form': form,
                           })

# Add a view which annotates and denotates tasks, as this can't be done by the
# task_update() method


def delete_task(request, task_id):
    """Deletes a task."""

    w.task_delete(id=task_id)
    return HttpResponseRedirect(reverse('list-tasks', args=['inbox']))


def documentation(request):
    """Shows documentation."""

    return render(request, 'documentation.html')


def configuration(request):
    """Shows configuration page."""

    return render(request, 'configuration.html')
