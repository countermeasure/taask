from django import forms


class AddTaskForm(forms.Form):

    description = forms.CharField(max_length=200)
    project = forms.CharField(max_length=200, required=False)
    priority = forms.CharField(max_length=200, required=False)
    due = forms.CharField(max_length=200, required=False)
    recur = forms.CharField(max_length=200, required=False)
    until = forms.CharField(max_length=200, required=False)
    wait = forms.CharField(max_length=200, required=False)
    scheduled = forms.CharField(max_length=200, required=False)
    depends = forms.CharField(max_length=200, required=False)
    # Add the necessary UDAs in here later
