from django import forms


class AddTaskForm(forms.Form):

    # 'description' is a string which describes the task
    description = forms.CharField(max_length=200)

    # 'view', a Taskwarrior UDA, is a string which defines the view
    VIEW_CHOICES = (
        ('inbox', 'Inbox'),
        ('today', 'Today'),
        ('next', 'Next'),
        ('someday', 'Someday'),
        )
    view = forms.ChoiceField(choices=VIEW_CHOICES, label='View')

    # 'priority' is a string which contains 'H', 'M' or 'L'
    # Either 'priority' or 'tag_importance' will be used longer term. 'priority'
    # should be preferred as it is the built-in option.
    PRIORITY_CHOICES = (
        (None, ''),
        ('H', 'High'),
        ('M', 'Medium'),
        ('L', 'Low'),
        )
    priority = forms.ChoiceField(choices=PRIORITY_CHOICES, required=False)

    # 'time', a Taskwarrior UDA, is a string which defines the estimated time
    # for a task
    TIME_CHOICES = (
        (None, ''),
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
    project = forms.CharField(max_length=200, required=False)

    # 'due' is a date on which the task should be finished
    due = forms.DateTimeField(required=False, label='Due date',
        widget=forms.TextInput(attrs={'class':'datepicker'})
        )

    # 'recur' is a string which represents the interval between recurring tasks,
    # such as '3wks'
    recur = forms.CharField(max_length=200, required=False, label='Frequency')

    # 'until' is a date on which a recurring task will cease to recur
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
    context_1 = forms.CharField(max_length=200, required=False,
                                label='Context 1')
    context_2 = forms.CharField(max_length=200, required=False,
                                label='Context 2')
    context_3 = forms.CharField(max_length=200, required=False,
                                label='Context 3')

class EditTaskForm(forms.Form):

    # 'description' is a string which describes the task
    description = forms.CharField(max_length=200)

    # 'view', a Taskwarrior UDA, is a string which defines the view
    VIEW_CHOICES = (
        ('inbox', 'Inbox'),
        ('today', 'Today'),
        ('next', 'Next'),
    # Take someday out of the list until it's clear what to do with it
    #   ('someday', 'Someday'),
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
    project = forms.CharField(max_length=200, required=False)

    # 'due' is a date on which the task should be finished
    due = forms.DateTimeField(required=False, label='Due date',
        widget=forms.TextInput(attrs={'class':'datepicker'})
        )

    # 'recur' is a string which represents the interval between recurring tasks,
    # such as '3wks'
    recur = forms.CharField(max_length=200, required=False, label='Frequency')

    # 'until' is a date on which a recurring task will cease to recur
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
    context_1 = forms.CharField(max_length=200, required=False,
                                label='Context 1')
    context_2 = forms.CharField(max_length=200, required=False,
                                label='Context 2')
    context_3 = forms.CharField(max_length=200, required=False,
                                label='Context 3')

