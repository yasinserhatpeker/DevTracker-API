from django.core.exceptions import ValidationError
from devtracker.models import Project,Task


def create_task(*,project_id:int,title:str) -> Task:
    if not Project.objects.filter(id=project_id).exists():
        raise ValidationError('Related project cannot be found.')
    
    task = Task.objects.create(project_id=project_id,title=title)
    return task


 
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
        
        

def toggle_task_status(*,task_id:int) -> Task:
    task = Task.objects.filter(id=task_id).first()
    
    if not task:
        raise ValidationError('Task cannot be found with this id')
    
    task.is_completed = not task.is_completed
    task.save()
    return task 



def delete_task(*,task_id:int) -> None:
    task = Task.objects.filter(id=task_id).first()
    if not task:
        raise ValidationError('Task cannot be found with this id')
    
    task.delete()
    
