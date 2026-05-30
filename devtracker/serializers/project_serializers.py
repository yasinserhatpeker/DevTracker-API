from rest_framework import serializers
from ..models import Project,Task


## WRITE SERIALIZERS 

class ProjectCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length = 200)
    description = serializers.CharField(required=False, allow_blank=True)
    

class ProjectUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(required=False, allow_blank =True)
    
    
    
## READ SERIALIZERS


class TaskOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id','title','is_completed','created_at')


class ProjectOutputSerializer(serializers.ModelSerializer):
    tasks = TaskOutputSerializer(many=True, read_only=True)
    class Meta:
        model = Project
        fields =('id','title','description','created_at','tasks')   
 
