from datetime import date

from django.core.signals import request_finished
from django.dispatch import receiver

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


@receiver(request_finished)
def manage_scheduled_tasks(sender, **kwargs):
    """Moves scheduled tasks which are scheduled for today or
    earlier into the 'Today' view.
    """
    scheduled_tasks = Task.objects.filter(view='scheduled')
    today = date.today()

    for task in scheduled_tasks:
        if task.scheduled <= today:
            task.scheduled = None
            task.view = 'today'
            task.save()
