import errno
import os
import shutil

from datetime import datetime

from django.core.management.base import BaseCommand

from tasks.models import Task


class Command(BaseCommand):
    help = 'Exports all tasks to a text file'

    def handle(self, *args, **options):
        HOME = os.environ['HOME']
        current_datetime = datetime.now()
        tasks = Task.objects.all().order_by('id').reverse()

        # Generate the snapshot file contents
        file_contents = '### TAASK TASKS ###\n'
        file_contents += '# Generated on %s\n\n' % \
            current_datetime.strftime('%d-%b-%Y @ %H:%M:%S')
        for task in tasks:
            contexts = []
            for context in task.context.all():
                contexts.append(str(context))
            task_string = '[description:"%s"\n' % task.description
            task_string += ' id:"%s"\n' % task.id
            if task.underway:
                task_string += ' underway:"%s"\n' % task.underway
            task_string += ' view:"%s"\n' % task.view
            if task.time:
                task_string += ' time:"%s"\n' % task.time
            if task.project:
                task_string += ' project:"%s"\n' % task.project
            if contexts:
                task_string += ' context:"%s"\n' % contexts
            if task.priority:
                task_string += ' priority:"%s"\n' % task.priority
            if task.scheduled:
                task_string += ' scheduled:"%s"\n' % task.scheduled
            if task.deadline:
                task_string += ' deadline:"%s"\n' % task.deadline
            if task.repeat_details:
                task_string += ' repeat details:"%s"\n' % task.repeat_details
            if task.repeat_ends:
                task_string += ' repeat ends:"%s"\n' % task.repeat_ends
            if task.repeat_every:
                task_string += ' repeat every:"%s"\n' % task.repeat_every
            if task.repeat_next:
                task_string += ' repeat next:"%s"\n' % task.repeat_next
            if task.repeat_units:
                task_string += ' repeat units:"%s"\n' % task.repeat_units
            if task.task:
                task_string += ' task:"%s"\n' % task.task
            if task.notes:
                task_string += ' notes:"%s"\n' % task.notes
            task_string += ' created:"%s"\n' % task.created
            task_string += ' modified:"%s"\n' % task.modified
            if task.completed:
                task_string += ' completed:"%s"\n' % task.completed
            task_string += ']\n'
            file_contents += task_string

        # Make sure the $HOME/.taask directory exists
        try:
            os.makedirs('%s/.taask/snapshots' % HOME)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

        # Create the snapshot file
        textfile = '%s/.taask/snapshots/taask_%s.txt' % \
            (HOME, current_datetime.strftime('%d%b%Y_at_%H%M%S'))
        with open(textfile, 'w') as f:
            f.write(file_contents)

        # Create the database snapshot
        database= '%s/.taask/taask.sqlite3' % HOME
        database_snapshot = '%s/.taask/snapshots/taask_%s.sqlite3' % \
            (HOME, current_datetime.strftime('%d%b%Y_at_%H%M%S'))
        shutil.copy(database, database_snapshot)
