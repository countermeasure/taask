from django import forms

from utils import get_choices, get_options


class BaseTaskForm(forms.Form):

    options = get_options()

    # 'description' is a string which describes the task
    description = forms.CharField(max_length=200)

    # 'view', a Taskwarrior UDA, is a string which defines the view
    VIEW_CHOICES = (
        ('inbox', 'Inbox'),
        ('today', 'Today'),
        ('next', 'Next'),
        ('scheduled', 'Scheduled'),
        ('recurring', 'Recurring'),
        ('someday', 'Someday'),
        ('rubbish', 'Rubbish'),
        )
    view = forms.ChoiceField(choices=VIEW_CHOICES, label='View')

    # 'priority' is a string which contains 'H', 'M' or 'L'
    PRIORITY_CHOICES = (
    #    (None, ''),
        ('H', 'High'),
        ('M', 'Medium'),
        ('L', 'Low'),
        )
    # If required is not set to False for priority, the form raises an error if
    # the task wasn't given a priority value on creation.
    priority = forms.ChoiceField(choices=PRIORITY_CHOICES, required=False)

    # 'order', a Taskwarrior UDA, is a string which defines the order of
    # tasks in the tables
    ORDER_CHOICES = (
        (None, ''),
        (1, '1st'),
        (2, '2nd'),
        (3, '3rd'),
        (4, '4th'),
        (5, '5th'),
        )
    order = forms.ChoiceField(choices=ORDER_CHOICES,
                              label='Order', required=False)

    # 'time', a Taskwarrior UDA, is a string which defines the estimated time
    # for a task
    TIME_CHOICES = (
        (5, '5mins'),
        (15, '15mins'),
        (30, '30mins'),
        (60, '1hr'),
        (120, '2hrs'),
        (300, '5hrs'),
        )
    time = forms.ChoiceField(choices=TIME_CHOICES, label='Time',
                             required=False)

    # 'project' is a string which gives the name of the project.
    projects = options['projects']
    PROJECT_CHOICES = get_choices(projects)
    project = forms.ChoiceField(choices=PROJECT_CHOICES, required=False)

    # 'due' is a date on which the task should be finished
    due = forms.DateTimeField(required=False, label='Due date',
        widget=forms.TextInput(attrs={'class':'datepicker'})
        )

    # 'recur' is a string which represents the interval between recurring tasks,
    # such as '3wks'
    recur = forms.CharField(max_length=200, required=False, label='Frequency')

    # 'until' is a date on which a task is automatically deleted. It is used to
    # set the date on which a recurring task will cease to recur
    until = forms.DateTimeField(required=False, label='Recurs until',
        widget=forms.TextInput(attrs={'class':'datepicker'})
        )

    # 'wait' is a date on which a task with status 'waiting' will have it's
    # status changed to 'pending'
    wait = forms.DateTimeField(required=False, label='Schedule for',
        widget=forms.TextInput(attrs={'class':'datepicker'})
        )

    # 'tags' is a list of strings, where each string is a single word containing
    # no spaces. For example:
    # ["home","garden"]
    # We'll collect several tags then merge them to create the tags list
    # The three 'context's will be stored in 'tags'
    contexts = options['contexts']
    CONTEXT_CHOICES = get_choices(contexts)
    context_1 = forms.ChoiceField(choices=CONTEXT_CHOICES, required=False,
                                label='Context 1')
    context_2 = forms.ChoiceField(choices=CONTEXT_CHOICES, required=False,
                                label='Context 2')
    context_3 = forms.ChoiceField(choices=CONTEXT_CHOICES, required=False,
                                label='Context 3')


    def clean(self):
        cleaned_data = super(BaseTaskForm, self).clean()

        # If the task is bypassing the inbox, it must have a priority and time
        if not cleaned_data.get('view') == 'inbox':
            if not cleaned_data.get('priority'):
                msg = u"This task must have a priority if it isn't going to" + \
                       " the inbox."
                self.add_error('priority', msg)
            if not cleaned_data.get('time'):
                msg = u"This task must have a time if it isn't going to the" + \
                       " inbox."
                self.add_error('time', msg)

        # If a wait date is set, the task must go in the scheduled view
        if cleaned_data.get('wait'):
            if cleaned_data.get('view') != 'scheduled':
                msg = u"This task's view must be 'scheduled'."
                self.add_error('view', msg)

        # If no wait date is set and the task is not a recurring one, the task
        # must not go in the scheduled view
        if not cleaned_data.get('wait') and not cleaned_data.get('until'):
            if cleaned_data.get('view') == 'scheduled':
                msg = u"This task's view must not be 'scheduled'."
                self.add_error('view', msg)

        # Contexts must not be duplicated
        if cleaned_data.get('context_1'):
            if cleaned_data.get('context_2') == cleaned_data.get('context_1'):
                msg = u"Context 2 must be different from Context 1."
                self.add_error('context_2', msg)
            if cleaned_data.get('context_3') == cleaned_data.get('context_1'):
                msg = u"Context 3 must be different from Context 1."
                self.add_error('context_3', msg)
        if cleaned_data.get('context_2'):
            if cleaned_data.get('context_3') == cleaned_data.get('context_2'):
                msg = u"Context 3 must be different from Context 2."
                self.add_error('context_3', msg)

        # There must be no blank context before another context
        if cleaned_data.get('context_2'):
            if not cleaned_data.get('context_1'):
                msg = u"Context 1 can't be empty if you set Context 2."
                self.add_error('context_1', msg)
        if cleaned_data.get('context_3'):
            if not cleaned_data.get('context_1'):
                msg = u"Context 1 can't be empty if you set Context 3."
                self.add_error('context_1', msg)
            if not cleaned_data.get('context_2'):
                msg = u"Context 2 can't be empty if you set Context 3."
                self.add_error('context_2', msg)

        # A scheduled task can't be due before it's scheduled date
        if cleaned_data.get('wait') and cleaned_data.get('due'):
            if cleaned_data.get('wait') > cleaned_data.get('due'):
                msg = u"Due date must be on or after the task's scheduled date."
                self.add_error('due', msg)

        # A recurring task mustn't have any information missing
        if cleaned_data.get('until'):
            if not cleaned_data.get('recur'):
                msg = u"A recurring task must have a frequency."
                self.add_error('recur', msg)
            if not cleaned_data.get('due'):
                msg = u"A recurring task must have a due date."
                self.add_error('due', msg)
        if cleaned_data.get('recur'):
            if not cleaned_data.get('until'):
                msg = u"A recurring task must have an end date."
                self.add_error('until', msg)
        if cleaned_data.get('due') and cleaned_data.get('recur'):
            if not cleaned_data.get('until'):
                msg = u"A recurring task must have an initial due date."
                self.add_error('due', msg)
        if cleaned_data.get('due') and cleaned_data.get('until'):
            if not cleaned_data.get('due'):
                msg = u"A recurring task must have a frequency (check)."
                self.add_error('recur', msg)

        # A recurring task's due date must be before its until (deletion) date
        if cleaned_data.get('due') and cleaned_data.get('until'):
            if cleaned_data.get('due') >= cleaned_data.get('until'):
                msg = u"Due date must be before the task's expiry date."
                self.add_error('due', msg)

        # A recurring task can't be scheduled for later
        if cleaned_data.get('until'):
            if cleaned_data.get('wait'):
                msg = u"A recurring task can't have a scheduled date set."
                self.add_error('wait', msg)

        # A recurring task must go in the recurring view
        if cleaned_data.get('until'):
            if cleaned_data.get('view') != 'recurring':
                msg = u"A recurring task's view must be 'recurring'."
                self.add_error('view', msg)


class AddTaskForm(BaseTaskForm):

    def __init__(self, *args, **kwargs):
        super(AddTaskForm, self).__init__(*args, **kwargs)


class EditTaskForm(BaseTaskForm):

    def __init__(self, *args, **kwargs):
        super(EditTaskForm, self).__init__(*args, **kwargs)
