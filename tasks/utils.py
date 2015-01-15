from models import Task


def get_task_count():
    """Returns a dictionary of the number of tasks in each view."""

    views_to_count = [
        'inbox',
        'today',
        'next',
        'scheduled',
        'someday',
        'recurring',
        'rubbish',
    ]

    task_count = {}
    for view in views_to_count:
        count = Task.objects.filter(view=view).count()
        task_count[view] = count

    return task_count
