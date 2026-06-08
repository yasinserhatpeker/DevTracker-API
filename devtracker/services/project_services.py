from django.core.exceptions import ValidationError
from devtracker.models import Project


def create_project(*,title:str,description:str="") -> Project:
    if Project.objects.filter(title=title).exists():
        raise ValidationError("This project is already exits")
    
    project = Project.objects.create(title=title,description=description)
    return project



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
 
 
def delete_project(*,project_id:int) -> None:
    project = Project.objects.filter(id=project_id).first()
    if not project:
        raise ValidationError('Project cannot be found with this id')
    
    project.delete()
    