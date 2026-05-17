from django.db.models import QuerySet
from .models import Project, Task

def get_projects() -> QuerySet[Project]:
    return Project.objects.prefetch_related('tasks').all() # avoiding n+1 problem with prefetch_related


def get_project_by_id(*,project_id:int) -> Project | None:
    return Project.objects.filter(id=project_id).first() # fetching related project


def get_tasks_by_project(*,project_id:int) -> QuerySet[Task]:
    return Task.objects.filter(project_id=project_id).first()  # fetching tasks by a project


