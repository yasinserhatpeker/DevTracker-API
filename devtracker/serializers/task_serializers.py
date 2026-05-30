from rest_framework import serializers
from ..models import Project,Task


## WRITE SERIALIZERS 

class TaskCreateSerializer(serializers.Serializer):
    project_id = serializers.IntegerField()
    title = serializers.CharField(max_length=200)

class TaskUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200, required=False)
    is_completed= serializers.BooleanField(required=False)
    
    
## READ SERIALIZERS



class TaskOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id','title','is_completed','created_at')


class ProjectOutputSerializer(serializers.ModelSerializer):
    task = TaskOutputSerializer(many=True, read_only=True)
    class Meta:
        model = Project
        fields =('id','title','description','created_at','task')   
 

    
    
    