from django.db.models import QuerySet
from  devtracker.models import Project, Task

def get_projects() -> QuerySet[Project]:
    return Project.objects.prefetch_related('tasks').all() # avoiding n+1 problem with prefetch_related


def get_project_by_id(*,project_id:int) -> Project | None:
     return Project.objects.prefetch_related('projects').get(id=project_id).first()
    
def get_tasks_by_project(*,project_id:int) -> QuerySet[Task]:
    return Task.objects.filter(project_id=project_id) # fetching tasks by a project
 

def get_task_by_id(*,task_id:int) -> Task | None:
    return Task.objects.get(id=task_id).first()
    
