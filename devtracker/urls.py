from django.urls import path
from .views import  (
    ProjectListApi,
    ProjectDetailApi,
    TaskListApi,
    TaskToggleApi,
    TaskDetailApi
)

urlpatterns = [
    #Project endpoint urls
    
    path('projects/', ProjectListApi.as_view(), name='Project-list'),
    path('projects/<int:project_id>/', ProjectDetailApi.as_view(), name='project-detail'),
    
    #Task endpoint urls
    
    path('tasks/', TaskListApi.as_view(), name='tasks-list'),
    path('tasks/<int:task_id>/', TaskDetailApi.as_view(), name='task-detail'),
    path('tasks/<int:task_id>/toggle/', TaskToggleApi.as_view(), name='task-toggle')
 ]