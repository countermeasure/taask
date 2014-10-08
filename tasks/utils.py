import yaml
from taskw import TaskWarrior


w = TaskWarrior()

def check_task_data():
    """Checks over the Taskwarrior data file to make sure it is up to date."""

    tasks = w.filter_tasks({'status': 'pending', 'view': None})

    # Move tasks which have status 'pending' but have no view data, which means
    # that the just stopped being scheduled, into the today view.
    for task in tasks:
        task['view'] = 'today'
        w.task_update(task)


def get_options():
    """Returns the contents of the twango.data file"""

    file = open('twango.config', 'r')
    options = yaml.load(file)

    return options


def get_choices(attribute):
    """Returns a tuple of choices for a form field"""

    # Start the list of choices with a None option, otherwise there is no option
    # to leave the field blank
    choices = [(None, '')]
    for choice in attribute:
        choice_tuple = choice, choice
        choices.append(choice_tuple)

    return choices


def get_task_count(projects):
    """Returns a dictionary of the number of tasks in each view."""

    views_to_count = [
        ('inbox', 'pending'),
        ('today', 'pending'),
        ('next', 'pending'),
        ('scheduled', 'waiting'),
        ('recurring', 'recurring'),
        ('someday', 'pending'),
        ('rubbish', 'pending'),
        ]

    for project in projects:
        views_to_count.append((project, 'all'))

    task_count = {}
    for view in views_to_count:
        tasks = w.filter_tasks({'view': view[0], 'status': view[1]})
        count = len(tasks)
        task_count[view[0]] = count

    return task_count


def manage_configuration(data, data_type):

    with open('twango.config', 'r') as f:
        config = yaml.load(f)

    action = data['action']
    tag = data['tag']

    if action == 'create':
        if data_type == 'context':
            config['contexts'].append(tag)
        elif data_type == 'project':
            config['projects'].append(tag)

    if action == 'delete':
        if data_type == 'context':
            config['contexts'].remove(tag)
        elif data_type == 'project':
            config['projects'].remove(tag)

    config['contexts'].sort()
    config['projects'].sort()

    with file('twango.config', 'w') as f:
        yaml.dump(config, f)
