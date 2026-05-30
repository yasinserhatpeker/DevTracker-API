from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from .views.auth_views import (
    LogoutApi,
    RegisterApi
)
from .views.project_views import (
    ProjectListApi,
    ProjectDetailApi,
) 
from .views.task_views import (
    TaskListApi,
    TaskDetailApi,
    TaskToggleApi
)


urlpatterns = [
    #Project endpoint urls
    
    path('projects/', ProjectListApi.as_view(), name='project-list'),
    path('projects/<int:project_id>/', ProjectDetailApi.as_view(), name='project-detail'),
    
    #Task endpoint urls
    
    path('tasks/', TaskListApi.as_view(), name='tasks-list'),
    path('tasks/<int:task_id>/', TaskDetailApi.as_view(), name='task-detail'),
    path('tasks/<int:task_id>/toggle/', TaskToggleApi.as_view(), name='task-toggle'),
    
    #Auth endpoint urls
    path('auth/register/', RegisterApi.as_view(), name='auth-register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='auth-login'),
    path('auth/refresh/',TokenRefreshView.as_view(), name='auth-refresh'),
    path('auth/logout/',LogoutApi.as_view(), name='auth-logout')
     
  
 ]