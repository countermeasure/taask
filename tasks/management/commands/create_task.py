from django.core.management.base import BaseCommand

from tasks.models import Task


class Command(BaseCommand):
    help = 'Creates a task'

    def add_arguments(self, parser):
        parser.add_argument('description', nargs='+', type=str)

    def handle(self, *args, **options):
        description = ' '.join([arg for arg in options['description']])
        task = Task.objects.create(description=description, view='inbox')

        self.stdout.write('Created task: %s' % task.description)
