from rest_framework import serializers
from devtracker.models import Project

## WRITE SERIALIZERS 

class TaskCreateSerializer(serializers.Serializer):
    project_id = serializers.PrimaryKeyRelatedField(queryset = Project.objects.all(),source='project')
    title = serializers.CharField(max_length=200)

class TaskUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200, required=False)
    is_completed= serializers.BooleanField(required=False)
    
    

    
    
    