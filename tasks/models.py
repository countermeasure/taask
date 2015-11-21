from  django.db import models


class TimeStampedModel(models.Model):
    """
    An abstract base class which provides self-updating
    'created' and 'modified' fields.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Task(TimeStampedModel):

    VIEW_CHOICES = (
        ('inbox', 'Inbox'),
        ('today', 'Today'),
        ('next', 'Next'),
        ('scheduled', 'Scheduled'),
        ('recurring', 'Recurring'),
        ('someday', 'Someday'),
        ('completed', 'Completed'),
        ('rubbish', 'Rubbish'),
    )
    REPEAT_UNITS_CHOICES = (
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    )

    completed = models.DateTimeField(
        blank=True,
        null=True,
    )
    description = models.CharField(
        max_length=200,
        blank=False,
    )
    deadline = models.DateField(
        blank=True,
        null=True,
    )
    repeat_details = models.CharField(
        max_length=200,
        blank=True,
        null=False,
    )
    repeat_ends = models.DateField(
        verbose_name='Repeats until',
        blank=True,
        null=True,
    )
    repeat_every = models.PositiveIntegerField(
        blank=True,
        null=True,
    )
    repeat_next = models.DateField(
        verbose_name='Next occurance',
        blank=True,
        null=True,
    )
    repeat_units = models.CharField(
        max_length=20,
        verbose_name='Create copies',
        choices=REPEAT_UNITS_CHOICES,
        blank=True,
        null=False,
    )
    notes = models.TextField(
        blank=True,
        null=False,
    )
    scheduled = models.DateField(
        verbose_name='Postpone until',
        blank=True,
        null=True,
    )
    time_remaining = models.PositiveIntegerField(
        blank=True,
        null=True,
    )
    time_spent = models.PositiveIntegerField(
        blank=True,
        null=True,
    )
    underway = models.BooleanField(default=False)
    view = models.CharField(
        max_length=50,
        choices=VIEW_CHOICES,
        default='inbox',
        blank=False,
    )
    context = models.ManyToManyField(
        'Context',
        blank=True,
        null=True,
    )
    priority = models.ForeignKey(
        'Priority',
        blank=True,
        null=True,
    )
    project = models.ForeignKey(
        'Project',
        blank=True,
        null=True,
    )
    task = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        related_name='child_tasks',
    )

    def __unicode__(self):
        return self.description


class Context(TimeStampedModel):
    context = models.CharField(
        max_length=50,
        unique = True,
        blank=False,
    )

    def __unicode__(self):
        return self.context

    class Meta:
        ordering = ['context']


class Project(TimeStampedModel):
    project = models.CharField(
        max_length=100,
        unique = True,
        blank=False,
    )

    def __unicode__(self):
        return self.project

    class Meta:
        ordering = ['project']


class Priority(TimeStampedModel):
    order = models.PositiveIntegerField(
        unique = True,
        blank = False,
    )
    priority = models.CharField(
        max_length=20,
        unique = True,
        blank=False,
    )

    def __unicode__(self):
        return self.priority

    class Meta:
        ordering = ['order']
