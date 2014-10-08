from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from tasks.forms import (AddTaskForm,
                        ContextForm,
                        EditTaskForm,
                        ProjectForm)
from tasks.utils import (check_task_data,
                         get_options,
                         get_task_count,
                         manage_configuration)
from taskw import TaskWarrior
from taskw.exceptions import TaskwarriorError


w = TaskWarrior(marshal=True)
# w = TaskWarrior(config_filename="/path/to/.taskrc")


def add_task(request):
    """Add a task."""

    tw_error = ''
    view = 'new_task'

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
            try:
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
                return HttpResponseRedirect(reverse('list-tasks', args=['today']))
            except TaskwarriorError, e:
                tw_error = str(e).rpartition('stderr:')[2].\
                           partition('; stdout')[0]

    else:
        form = AddTaskForm(label_suffix='')

    options = get_options()
    projects = options['projects']
    contexts = options['contexts']

    task_count = get_task_count(projects)

    return render(request, 'add_task.html', {
                           'view': view,
                           'task_count': task_count,
                           'projects': projects,
                           'contexts': contexts,
                           'tw_error': tw_error,
                           'form': form,
                           })


def list_tasks(request, view):
    """Shows a filtered list of tasks.

       filter_tasks() returns a list which contains one dictionary per task."""

    options = get_options()
    projects = options['projects']
    contexts = options['contexts']

    check_task_data()

    if view in ['inbox', 'today', 'next', 'someday', 'rubbish']:
        task_list = w.filter_tasks({'status': 'pending', 'view': view,})

    elif view == 'scheduled':
        task_list = w.filter_tasks({'status': 'waiting',})

    elif view == 'recurring':
        task_list = w.filter_tasks({'status': 'recurring',})

    elif view == 'completed':
        task_list = w.filter_tasks({'status': 'completed',})

    else:
        for project in projects:
            if view == project.lower():
                task_list = w.filter_tasks({'project': project,})

    # Examples of sorting
    # task_list.sort(key = lambda task : task['description'].lower())
    # task_list.sort(key = lambda task : task['tags'][2])

    task_count = get_task_count(projects)

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
            # Update the task
            w.task_update(task)
            return HttpResponseRedirect(reverse('list-tasks', args=['today']))
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

    options = get_options()
    projects = options['projects']
    contexts = options['contexts']

    task_count = get_task_count(projects)

    return render(request, 'edit_task.html', {
                           'task_count': task_count,
                           'projects': projects,
                           'contexts': contexts,
                           'task_id': task_id,
                           'form': form,
                           })

# Add a view which annotates and denotates tasks, as this can't be done by the
# task_update() method

def complete_task(request, task_id):
    """Completes a task."""

    id, task = w.get_task(id=task_id)
    # Only complete tasks from certain views
    if task['view'] in ['inbox', 'today', 'next', 'someday']:
        task['view'] = 'completed'
        w.task_update(task)
        w.task_done(id=task_id)

    return HttpResponseRedirect(reverse('list-tasks', args=['today']))


def delete_task(request, task_id):
    """Deletes a task."""

    # Check that the tasks is in the 'rubbish' view before deleting it
    id, task = w.get_task(id=task_id)
    if task['view'] == 'rubbish':
        w.task_delete(id=task_id)

    return HttpResponseRedirect(reverse('list-tasks', args=['today']))


def documentation(request):
    """Shows documentation."""

    return render(request, 'documentation.html')


def configuration(request):
    """Shows configuration page."""

    if request.method == "POST":

        context_form = ContextForm(request.POST, prefix='context',
                                   label_suffix='')
        if context_form.is_valid():
            data = context_form.cleaned_data
            manage_configuration(data, 'context')

        project_form = ProjectForm(request.POST, prefix='project',
                                   label_suffix='')
        if project_form.is_valid():
            data = project_form.cleaned_data
            manage_configuration(data, 'project')

    else:
        context_form = ContextForm(prefix='context')
        project_form = ProjectForm(prefix='project')

    options = get_options()

    return render(request, 'configuration.html', {
                           'options': options,
                           'context_form': context_form,
                           'project_form': project_form,
                           })

