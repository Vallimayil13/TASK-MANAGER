from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('DONE', 'Done'),
    ]

    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES,default='Pending')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES,default='Medium')

    # created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


