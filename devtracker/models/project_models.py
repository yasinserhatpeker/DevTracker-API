from django.db import models

class Project(models.Model): # Project entity
    title = models.CharField(max_length=200)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='projects')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.title
