from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from tasks.forms import AddTaskForm, EditTaskForm
from tasks.utils import check_task, \
                        get_options, \
                        get_task_count
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
            view = form.cleaned_data['view']
            priority = form.cleaned_data['priority']
            time = form.cleaned_data['time']
            project = form.cleaned_data['project']
            due = form.cleaned_data['due']
            recur = form.cleaned_data['recur']
            until = form.cleaned_data['until']
            wait = form.cleaned_data['wait']
            context_1 = form.cleaned_data['context_1']
            context_2 = form.cleaned_data['context_2']
            context_3 = form.cleaned_data['context_3']
            # Context data is held in Taskwarrior's 'tags' field
            # Construct 'tags' in the format which taskw expects
            tags = [context_1, context_2, context_3]
            # Create the new task
            w.task_add(description,
                       view=view,
                       priority=priority,
                       time=time,
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
        task_list = w.filter_tasks({'status': 'pending', 'view': view,})

    elif view == 'scheduled':
        task_list = w.filter_tasks({'status': 'waiting',})

    elif view == 'completed':
        task_list = w.filter_tasks({'status': 'completed',})

    # Examples of sorting
    # task_list.sort(key = lambda task : task['description'].lower())
    # task_list.sort(key = lambda task : task['tags'][2])

    task_count = get_task_count()

    options = get_options()
    projects = options['projects']
    contexts = options['contexts']

    # import pdb; pdb.set_trace()

    return render(request, 'list_tasks.html', {
                           'task_list': task_list,
                           'task_count': task_count,
                           'projects': projects,
                           'contexts': contexts,
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
                              'view',
                              'priority',
                              'order',
                              'time',
                              'project',
                              'due',
                              'recur',
                              'until',
                              'wait']
            for attribute in non_tag_fields:
                value = form.cleaned_data[attribute]
                # The time and order variables must be integers to be saved into
                # the task dictionary
                if attribute in ['time', 'order']:
                    if value:
                        value = int(value)
                    else:
                        value = 0
                task[attribute] = value
            # Create the tag attribute in the format which taskw expects and
            # write it to the task
            tag_fields = ['context_1',
                          'context_2',
                          'context_3']
            tags = []
            for attribute in tag_fields:
                value = form.cleaned_data[attribute]
                tags.append(value)
            task['tags'] = tags
            # Check that the modifications to the task make sense, and fix any
            # that don't
            task = check_task(task)
            # Update the task
            w.task_update(task)
            return HttpResponseRedirect(reverse('list-tasks', args=['inbox']))
    else:
        # Add each individual tag item to the task object so that they are
        # displayed in the form
        tags = task['tags']
        task['context_1'] = tags[0]
        task['context_2'] = tags[1]
        task['context_3'] = tags[2]
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

    # Check that the tasks is in the 'rubbish' view before deleting it
    id, task = w.get_task(id=task_id)
    if task['view'] == 'rubbish':
        w.task_delete(id=task_id)

    return HttpResponseRedirect(reverse('list-tasks', args=['inbox']))


def documentation(request):
    """Shows documentation."""

    return render(request, 'documentation.html')


def configuration(request):
    """Shows configuration page."""

    return render(request, 'configuration.html')
