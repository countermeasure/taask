from datetime import date

from django import forms

from models import (
    Context,
    Priority,
    Project,
    Task,
)


class TaaskModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("label_suffix", "")
        super(TaaskModelForm, self).__init__(*args, **kwargs)


class TaskForm(TaaskModelForm):

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.VIEW_CHOICES = (
            ('inbox', 'Inbox'),
            ('today', 'Today'),
            ('next', 'Next'),
            ('scheduled', 'Scheduled'),
            ('recurring', 'Recurring'),
            ('someday', 'Someday'),
            ('completed', 'Completed'),
            )
        self.fields['view'].choices = self.VIEW_CHOICES

    class Meta:
        model = Task
        fields = [
            'context',
            'deadline',
            'description',
            'repeat_ends',
            'repeat_every',
            'repeat_next',
            'repeat_units',
            'notes',
            'priority',
            'project',
            'scheduled',
            'time_remaining',
            'time_spent',
            'underway',
            'view',
        ]
        widgets = {
            'context': forms.CheckboxSelectMultiple(),
            'priority': forms.RadioSelect(),
            'project': forms.RadioSelect(),
            'view': forms.RadioSelect(),
        }

    def clean(self):
        cleaned_data = super(TaskForm, self).clean()

        # If the task is not going to inbox, it must have a priority and
        # context and time remaining must not be None
        if not cleaned_data.get('view') == 'inbox':
            if not cleaned_data.get('priority'):
                # Don't require completed tasks to have a priority though
                if not cleaned_data.get('view') == 'completed':
                    msg = (u"This task must have a priority if it isn't going "
                           u"to 'Inbox'.")
                    self.add_error('priority', msg)
            if cleaned_data.get('time_remaining') is None:
                self.add_error('time_remaining', u"This task must have a time "
                               u"remaining if it isn't going to 'Inbox'.")
            if not cleaned_data.get('context'):
                self.add_error('context', u"This task must have at least one "
                                       u"context if it isn't going to 'Inbox'.")

        # A completed task which is being edited can't have a priority added
        if cleaned_data.get('view') == 'completed':
            if cleaned_data.get('priority'):
                msg = u"A completed task can't have a priority."
                self.add_error('priority', msg)

        # If a scheduled date is set, the task must go in the scheduled view
        if cleaned_data.get('scheduled'):
            if cleaned_data.get('view') != 'scheduled':
                self.add_error('view', u"This task's view must be 'Scheduled'.")

        # If no scheduled date is set, the task must not go in the scheduled
        # view
        if not cleaned_data.get('scheduled'):
            if cleaned_data.get('view') == 'scheduled':
                msg = u"This task's view must not be 'Scheduled'."
                self.add_error('view', msg)

        # A scheduled task's deadline can't be before it's scheduled date
        if cleaned_data.get('scheduled') and cleaned_data.get('deadline'):
            if cleaned_data.get('scheduled') > cleaned_data.get('deadline'):
                self.add_error('deadline', u"Deadline must be on or after the "
                                      u"task's 'Postpone until' date.")

        # A recurring task mustn't have any information missing
        if (cleaned_data.get('repeat_details') or
            cleaned_data.get('repeat_ends') or
            cleaned_data.get('repeat_every') or
            cleaned_data.get('repeat_next') or
            cleaned_data.get('repeat_units')):
            # if not cleaned_data.get('repeat_details'):
            #     msg = u"A recurring task must have repeat details."
            #     self.add_error('repeat_details', msg)
            if not cleaned_data.get('repeat_ends'):
                msg = u"A recurring task must have an end date."
                self.add_error('repeat_ends', msg)
            if not cleaned_data.get('repeat_every'):
                msg = u"A recurring task must have 'Repeat every' set."
                self.add_error('repeat_every', msg)
            if not cleaned_data.get('repeat_next'):
                msg = u"A recurring task must have a next date."
                self.add_error('repeat_next', msg)
            if not cleaned_data.get('repeat_units'):
                msg = u"A recurring task must have repeat units."
                self.add_error('repeat_units', msg)

        # A recurring task can't have a deadline
        # TODO: Allow recurring tasks to have deadlines
        if cleaned_data.get('deadline') and cleaned_data.get('repeat_ends'):
            msg = u"At the moment, recurring tasks can't have deadlines."
            self.add_error('deadline', msg)

        # A recurring task's next date can't be before it's end date
        if cleaned_data.get('repeat_next'):
            if cleaned_data.get('repeat_next') > cleaned_data.get('repeat_ends'):
                msg = u"A repeating task must not end before the next date"
                self.add_error('repeat_ends', msg)

        # A recurring task can't be scheduled for later
        if cleaned_data.get('repeat_ends'):
            if cleaned_data.get('scheduled'):
                msg = u"A recurring task can't have a 'Postpone until' date set."
                self.add_error('scheduled', msg)

        # A recurring task must go in the recurring view
        if cleaned_data.get('repeat_ends'):
            if cleaned_data.get('view') != 'recurring':
                msg = u"A recurring task's view must be set to 'Recurring'."
                self.add_error('view', msg)

        # A task can't be scheduled on or before today's date
        if cleaned_data.get('scheduled'):
            if cleaned_data.get('scheduled') <= date.today():
                msg = u"A task can only be scheduled for a future date."
                self.add_error('scheduled', msg)

        # A task can only be underway if it is in the 'Today' view
        if cleaned_data.get('underway'):
            if cleaned_data.get('view') != 'today':
                msg = u"A task must be in 'Today' to be underway."
                self.add_error('underway', msg)


class ContextForm(TaaskModelForm):

    class Meta:
        model = Context
        fields = ['context']


class PriorityForm(TaaskModelForm):

    class Meta:
        model = Priority
        fields = [
            'priority',
            'order',
        ]

class ProjectForm(TaaskModelForm):

    class Meta:
        model = Project
        fields = ['project']
