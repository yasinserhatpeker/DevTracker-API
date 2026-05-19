from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Project,Task


## CREATE 

def create_project(*,title:str,description:str="") -> Project:
    if Project.objects.filter(title=title).exists():
        raise ValidationError("This project is already exits")
    
    project = Project.objects.create(title=title,description=description)
    return project


def create_task(*,project_id:str,title:str) -> Task:
    if not Project.objects.filter(id=project_id).exists():
        raise ValidationError('Related project cannot be found.')
    
    task = Task.objects.create(project_id=project_id,title=title)
    return task


def create_user(*,username:str,email:str,password:str) -> User:
    if User.objects.filter(username=username).exists():
        raise ValidationError('This username is taken.')
    if User.objects.filter(email=email).exists():
        raise ValidationError('This email is taken.')
    
    user = User.objects.create_user(username=username,email=email,password=password)
    return user
    

## UPDATE


def update_project(*,project_id:int,title:str,description:str)-> Project:
     project = Project.objects.filter(id=project_id).first()
     
     if not project:
         raise ValidationError('Project cannot be found.')
     
     if Project.objects.exclude(id=project_id).filter(title=title).exists():
         raise ValidationError('The project with this title is already exist.')
     
     project.title=title
     project.description=description
     
     project.save()
     return project
 
 
def update_task(*,task_id:int,title:str = None, is_completed:bool = None, project_id:int = None) -> Task:
    task = Task.objects.filter(id=task_id).first()
    if not task:
        raise ValidationError('Task cannot be found with this id')
    
    if project_id is not None:
        if not Project.objects.filter(id=project_id).exists():
            raise ValidationError("Project cannot be found.")
        task.project_id = project_id
    
    if title is not None:
        task.title = title
        
    if is_completed is not None:
        task.is_completed = is_completed
        
    task.save()
    return task
        
        
## TOGGLE TASK STATUS

def toggle_task_status(*,task_id:int) -> Task:
    task = Task.objects.filter(id=task_id).first()
    
    if not task:
        raise ValidationError('Task cannot be found with this id')
    
    task.is_completed = not task.is_completed
    task.save()
    return task 



## DELETE

def delete_project(*,project_id:int) -> None:
    project = Project.objects.filter(id=project_id).first()
    if not project:
        raise ValidationError('Project cannot be found with this id')
    
    project.delete()
    

def delete_task(*,task_id:int) -> None:
    task = Task.objects.filter(id=task_id).first()
    if not task:
        raise ValidationError('Task cannot be found with this id')
    
    task.delete()
    

     
     