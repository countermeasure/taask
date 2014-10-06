import yaml
from taskw import TaskWarrior


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


def get_task_count():
    """Returns a dictionary of the number of tasks in each view."""

    w = TaskWarrior()

    inbox_tasks = w.filter_tasks({'status': 'pending', 'view': 'inbox',})
    inbox_count = len(inbox_tasks)
    task_count = {'inbox': inbox_count}

    today_tasks = w.filter_tasks({'status': 'pending', 'view': 'today',})
    today_count = len(today_tasks)
    task_count['today'] = today_count

    next_tasks = w.filter_tasks({'status': 'pending', 'view': 'next',})
    next_count = len(next_tasks)
    task_count['next'] = next_count

    scheduled_tasks = w.filter_tasks({'status': 'wait', 'view': 'scheduled',})
    scheduled_count = len(scheduled_tasks)
    task_count['scheduled'] =scheduled_count

    recurring_tasks = w.filter_tasks({'status': 'recurring',
                                      'view': 'recurring',})
    recurring_count = len(recurring_tasks)
    task_count['recurring'] = recurring_count

    someday_tasks = w.filter_tasks({'status': 'pending', 'view': 'someday',})
    someday_count = len(someday_tasks)
    task_count['someday'] = someday_count

    rubbish_tasks = w.filter_tasks({'status': 'pending', 'view': 'rubbish',})
    rubbish_count = len(rubbish_tasks)
    task_count['rubbish'] = rubbish_count

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

    config['contexts'].sort()
    config['projects'].sort()

    with file('twango.config', 'w') as f:
        yaml.dump(config, f)
