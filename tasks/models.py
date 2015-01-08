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
    description = models.CharField(
        max_length=200,
        null=False,
    )
    notes = models.TextField(null=True)
    view = models.CharField(
        max_length=50,
        null=False,
    )
    time = models.PositiveIntegerField(null=True)
    priority = models.ForeignKey(
        'Priority',
        null=True,
    )
    due = models.DateTimeField(null=True)
    project = models.ForeignKey(
        'Project',
        null=True,
    )
    context = models.ForeignKey(
        'Context',
        null=True,
    )
    scheduled = models.DateTimeField(null=True)
    status = models.CharField(
        max_length=20,
        null=False,
    )
    active = models.BooleanField(default=False)
    frequency = models.CharField(
        max_length=50,
        null=True,
        blank=False,
    )
    ends = models.DateTimeField(null=True)
    task = models.ForeignKey(
        'Task',
        null=True,
        related_name='child_tasks',
    )

    def __unicode__(self):
        return self.description


class Context(TimeStampedModel):
    context = models.CharField(
        max_length=50,
        null=True,
    )

    def __unicode__(self):
        return self.context


class Project(TimeStampedModel):
    project = models.CharField(
        max_length=100,
        null=True,
    )

    def __unicode__(self):
        return self.project


class Priority(TimeStampedModel):
    priority = models.CharField(
        max_length=20,
        null=True,
    )

    def __unicode__(self):
        return self.priority
