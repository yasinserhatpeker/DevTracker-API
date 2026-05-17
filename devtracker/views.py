from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError

from . import selectors,services
from .serializers import (
    ProjectCreateSerializer,
    ProjectUpdateSerializer,
    ProjectOutputSerializer,
    TaskCreateSerializer,
    TaskUpdateSerializer,
    TaskOutputSerializer
)

## Project List API

class ProjectListApi(APIView): 
    """
    Route: /api/projects/
    """
    
    def get(self,request):
        
        projects = selectors.get_projects() # Read Query
        
        serializer = ProjectOutputSerializer(projects,many=True) # Converts to JSON
        
        return Response(serializer.data, status = status.HTTP_200_OK) # returns a response
    
    def post(self,request):
        
        serializer = ProjectCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            new_project = services.create_project(
                title = serializer.validated_data['title'],
                description = serializer.validated_data.get('description','')
                
            )
            output_serializer = ProjectOutputSerializer(new_project)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        
        except ValidationError as e:
            return Response({"list":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
        
        
## Project Detail API

class ProjectDetailAPI(APIView):
    """
    Route: /api/projects/<int:project_id>/
    """
    
    def put(self,request,project_id):
        serializer = ProjectUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            updated_project = services.update_project(
                project_id=project_id,
                title = serializer.validated_data['title'],
                description= serializer.validated_data.get('description','')
            )
            
            output_serializer = ProjectOutputSerializer(updated_project)
            return Response(output_serializer.data, status = status.HTTP_200_OK)
        
        except ValidationError as e:
            return Response({"detail":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
    
    def delete(self,request,project_id):
        try:
            services.delete_project(project_id=project_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        except ValidationError as e:
            return Response({"detail":str(e)}, status=status.HTTP_400_BAD_REQUEST) 
        


class TaskListApi(APIView):
    """
    Route: /api/tasks/
    """
    
    def post(self,request):
        serializer = TaskCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            new_task = services.create_task(
                project_id=serializer.validated_data['project_id'],
                title=serializer.validated_data['title']
            )
            output_serializer = TaskOutputSerializer(new_task)
            return Response(output_serializer.data,status=status.HTTP_201_CREATED)
        
        except ValidationError as e:
            return Response({"detail":str(e)}, status=status.HTTP_400_BAD_REQUEST) 
        
        
    
class TaskDetailAPI(APIView):
    """
    Route: /api/tasks/<int:task_id>
    """
    
    def put(self, request, task_id):
        serializer = TaskUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            updated_task = services.update_task(
                task_id=task_id,
                title=serializer.validated_data.get('title'),
                is_completed=serializer.validated_data.get('is_completed'),
                project_id=serializer.validated_data.get('project_id')
            )
            
            output_serializer = TaskOutputSerializer(updated_task)
            return Response(output_serializer.data, status=status.HTTP_200_OK)
        
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
        
    def delete(self,task_id):
        services.delete_task(task_id=task_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    

    
    
        