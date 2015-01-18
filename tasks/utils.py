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


def process_and_save_task(task, form):
    """Processes a task form to ensur that the data it generates
    is internally consistent, then save it.
    """
    #import pdb; pdb.set_trace()

    updated_task = form.save(commit=False)
    # When a completed task is moved to another view, set its
    # 'completed' attribute to 'None'
    if task.completed and (form.cleaned_data['view'] != 'completed'):
        updated_task.completed = None

    updated_task.save()
    form.save_m2m()


@receiver(request_finished)
def manage_dated_tasks(sender, **kwargs):
    """Moves scheduled or deadlined tasks to the 'Today' view
    when appropriate.
    """
    scheduled_tasks = Task.objects.filter(view='scheduled')
    deadlined_tasks = Task.objects.exclude(deadline=None)
    today = date.today()

    # Move scheduled tasks to 'Today' if they are scheduled on
    # or before today's date
    for task in scheduled_tasks:
        if task.scheduled <= today:
            task.scheduled = None
            task.view = 'today'
            task.save()

    # Move deadlined tasks to 'Today' if their deadline is on
    # or before today's date and they are not completed
    for task in deadlined_tasks:
        if (task.deadline <= today) and \
            (task.view not in ['today', 'completed']):
                task.view = 'today'
                task.save()
