from django.core.exceptions import ValidationError
from .models import Project,Task

## CREATE 

def create_project(*,title:str,description:str="") -> Project:
    if Project.objects.filter(title=title).exists():
        raise ValidationError("This project is already exits")
    
    project = Project.objects.create(title=title,description=description)
    return project


def create_task(*,project_id:str,title:str) -> Task:
    if not Task.objects.filter(id=project_id).exists():
        raise ValidationError('Task cannot be found.')
    
    task = Task.objects.create(project_id=project_id,title=title)
    return task