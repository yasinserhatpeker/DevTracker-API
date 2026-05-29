from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from . import selectors,services
from .serializers import (
    ProjectCreateSerializer,
    ProjectUpdateSerializer,
    ProjectOutputSerializer,
    TaskCreateSerializer,
    TaskUpdateSerializer,
    TaskOutputSerializer,
    RegisterSerializer
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

class ProjectDetailApi(APIView):
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
        
        
    
class TaskDetailApi(APIView):
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
        
        
        
    def delete(self,request,task_id):
       try:
            services.delete_task(task_id=task_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
       except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    
    
    
## TaskToggleApi

class TaskToggleApi(APIView):
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
    
           
            
## User 

class RegisterApi(APIView):
    """
    Route: /api/auth/register/
    """
    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            services.create_user(
                username=serializer.validated_data['username'],
                email=serializer.validated_data.get('email',''),
                password=serializer.validated_data['password']
                )
            return Response({"detail":"Register successfully"},status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"detail":str(e)},status=status.HTTP_400_BAD_REQUEST)
        
    
class LogoutApi(APIView):
    """
    Route: /api/auth/logout/
    """
    def post(self,request):
       try:
           refresh_token = request.data.get('refresh')
           if not refresh_token:
              return Response({"detail":"Refresh token is mandatory"}, status=status.HTTP_400_BAD_REQUEST)
          
           token = RefreshToken(refresh_token)
           token.blacklist()
           
           return Response({"detail":"Logout successfully"},status=status.HTTP_205_RESET_CONTENT)
       
       except Exception:
           return Response({"detail":"Invalid token:"},status=status.HTTP_400_BAD_REQUEST)   
    
        