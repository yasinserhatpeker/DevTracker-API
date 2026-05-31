from django.db import models

class Task(models.Model): # Task entity
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return (f"{self.title} - {'is finished' if self.is_completed else 'is pending...'}")

  