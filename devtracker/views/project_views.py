from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError
from .. import selectors,services
from devtracker.serializers import (
    ProjectCreateSerializer,
    ProjectOutputSerializer,
    ProjectUpdateSerializer
       
)
## Project List API

class ProjectListApi(APIView): 
    permission_classes=[IsAuthenticated]
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
    permission_classes=[IsAuthenticated]
    """
    Route: /api/projects/<int:project_id>/
    """
    
    def get(self,request,project_id): 
        
        project = selectors.get_project_by_id(project_id=project_id)
        if not project:
              return Response({"detail":"Project not found"}, status=status.HTTP_400_BAD_REQUEST)
          
        output_serializer = ProjectOutputSerializer(project)
        return Response(output_serializer.data, status=status.HTTP_200_OK)
        
        
    
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