from django.db.models import QuerySet
from  devtracker.models import Project, Task

def get_projects() -> QuerySet[Project]:
    return Project.objects.prefetch_related('tasks').all() # avoiding n+1 problem with prefetch_related


def get_project_by_id(*,project_id:int) -> Project | None:
     try:
         return Project.objects.get(id=project_id)
     except Project.DoesNotExist:
         return None


def get_tasks_by_project(*,project_id:int) -> QuerySet[Task]:
    return Task.objects.filter(project_id=project_id) # fetching tasks by a project
 

def get_task_by_id(*,task_id:int) -> Task | None:
    try:
        return Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return None
