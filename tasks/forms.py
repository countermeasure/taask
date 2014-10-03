from django import forms


class AddTaskForm(forms.Form):

    # 'description' is a string which describes the task
    description = forms.CharField(max_length=200)

    # 'tags' is a list of strings, where each string is a single word containing
    # no spaces. For example:
    # ["home","garden"]
    # We'll collect several tags then merge them to create the tags list

    # Tag which defines the view
    VIEW_CHOICES = (
        ('inbox', 'Inbox'),
        ('today', 'Today'),
        ('next', 'Next'),
        ('someday', 'Someday'),
        )
    tag_view = forms.ChoiceField(choices=VIEW_CHOICES,
                                 label='View')

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

    # Tag which defines the estimated time for a task
    TIME_CHOICES = (
        (None, ''),
        ('5', '5mins'),
        ('15', '15mins'),
        ('30', '30mins'),
        ('60', '1hr'),
        ('120', '2hrs'),
        ('300', '5hrs'),
        )
    tag_time = forms.ChoiceField(choices=TIME_CHOICES, label='Time',
                                 required=False)

    # 'project' is a string which gives the name of the project.
    project = forms.CharField(max_length=200, required=False)

    # 'due' is a date on which the task should be finished
    due = forms.DateTimeField(required=False, label='Due date')

    # 'recur' is a string which represents the interval between recurring tasks,
    # such as '3wks'
    recur = forms.CharField(max_length=200, required=False, label='Frequency')

    # 'until' is a date on which a recurring task will cease to recur
    until = forms.DateTimeField(required=False, label='Recurs until')

    # 'wait' is a date on which a task with status 'waiting' will have it's
    # status changed to 'pending'
    wait = forms.DateTimeField(required=False, label='Schedule for')


class EditTaskForm(forms.Form):

    # 'description' is a string which describes the task
    description = forms.CharField(max_length=200)

    # 'tags' is a list of strings, where each string is a single word containing
    # no spaces. For example:
    # ["home","garden"]
    # We'll collect several tags then merge them to create the tags list

    # Tag which defines the view
    VIEW_CHOICES = (
        ('inbox', 'Inbox'),
        ('today', 'Today'),
        ('next', 'Next'),
        ('someday', 'Someday'),
        ('rubbish', 'Rubbish'),
        )
    tag_view = forms.ChoiceField(choices=VIEW_CHOICES,
                                 label='View')

    # 'priority' is a string which contains 'H', 'M' or 'L'
    PRIORITY_CHOICES = (
    #    (None, ''),
        ('H', 'High'),
        ('M', 'Medium'),
        ('L', 'Low'),
        )
    priority = forms.ChoiceField(choices=PRIORITY_CHOICES)

    # Tag which defines the order of tasks in the tables
    ORDER_CHOICES = (
        (None, ''),
        ('first', '1st'),
        ('second', '2nd'),
        ('third', '3rd'),
        ('fourth', '4th'),
        ('fifth', '5th'),
        )
    tag_order = forms.ChoiceField(choices=ORDER_CHOICES,
                                  label='Order', required=False)

    # Tag which defines the estimated time for a task
    TIME_CHOICES = (
        (None, ''),
        ('5', '5mins'),
        ('15', '15mins'),
        ('30', '30mins'),
        ('60', '1hr'),
        ('120', '2hrs'),
        ('300', '5hrs'),
        )
    tag_time = forms.ChoiceField(choices=TIME_CHOICES, label='Time',
                                 required=False)

    # 'project' is a string which gives the name of the project.
    project = forms.CharField(max_length=200, required=False)

    # 'due' is a date on which the task should be finished
    due = forms.DateTimeField(required=False, label='Due date')

    # 'recur' is a string which represents the interval between recurring tasks,
    # such as '3wks'
    recur = forms.CharField(max_length=200, required=False, label='Frequency')

    # 'until' is a date on which a recurring task will cease to recur
    until = forms.DateTimeField(required=False, label='Recurs until')

    # 'wait' is a date on which a task with status 'waiting' will have it's
    # status changed to 'pending'
    wait = forms.DateTimeField(required=False, label='Schedule for')
