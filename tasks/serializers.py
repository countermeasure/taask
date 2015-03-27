from rest_framework import serializers
from models import (
    Context,
    Task,
)


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = (
            'id',
            'completed',
            'description',
            'deadline',
            'repeat_details',
            'repeat_ends',
            'repeat_every',
            'repeat_next',
            'repeat_units',
            'notes',
            'scheduled',
            'time_remaining',
            'time_spent',
            'underway',
            'view',
            'context',
            'priority',
            'project',
            'task',
        )


class ContextSerializer(serializers.ModelSerializer):

    class Meta:
        model = Context
        fields = (
            'id',
            'context',
        )
