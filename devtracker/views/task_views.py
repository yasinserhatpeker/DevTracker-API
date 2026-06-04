from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from ..services import services
from .. import selectors
from devtracker.serializers import(
    TaskCreateSerializer,
    TaskOutputSerializer,
    TaskUpdateSerializer
)

class TaskListApi(APIView):
    permission_classes=[IsAuthenticated]
    """
    Route: /api/tasks/
    """
    def get(self,request):
        tasks = selectors.get_tasks_by_project(user=request.user)
        if not tasks:
           return Response({"detail":"There's no task related to project"}, status=status.HTTP_400_BAD_REQUEST) 
    
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
        
        
    
class TaskDetailApi(APIView):
    permission_classes=[IsAuthenticated]
    """
    Route: /api/tasks/<int:task_id>
    """
    
    def get(self,request,task_id):
        task = selectors.get_task_by_id(task_id=task_id)
        if not task:
            return Response({"detail":"Task not found"}, status=status.HTTP_404_NOT_FOUND)
        
        output_serializer = TaskOutputSerializer(task)
        return Response(output_serializer.data, status=status.HTTP_200_OK)
    
    
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
        
        
        
    def delete(self,request,task_id):
       try:
            services.delete_task(task_id=task_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
       except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    
    
    
## TaskToggleApi

class TaskToggleApi(APIView):
    permission_classes=[IsAuthenticated]
    """
    Route: /api/tasks/<int:task_id>/toggle/
    """
    def post(self,request,task_id):
        try:
            
           updated_task=services.toggle_task_status(task_id=task_id)
           output_serializer = TaskOutputSerializer(updated_task)
           
           return Response(output_serializer.data,status=status.HTTP_200_OK)
       
        except ValidationError as e:
           return Response({"detail":str(e)},status=status.HTTP_400_BAD_REQUEST)
    
    
        