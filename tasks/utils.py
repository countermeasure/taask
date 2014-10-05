import yaml
from taskw import TaskWarrior


def get_options():
    """Returns the contents of the twango.data file"""

    file = open('twango.config', 'r')
    options = yaml.load(file)

    return options


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

    rubbish_tasks = w.filter_tasks({'status': 'pending', 'view': 'rubbish',})
    rubbish_count = len(rubbish_tasks)
    task_count['rubbish'] = rubbish_count

    return task_count
