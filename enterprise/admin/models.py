from django.db import models
from employee.models import *
from dept_head.models import *
from manager.models import *

# Create your models here.

class user(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField()
    role = models.CharField(max_length=50, choices=[('admin', 'Admin'), ('manager', 'Manager'), ('dept_head', 'Department Head'), ('employee', 'Employee')])
    is_active = models.BooleanField(default=True)
    ragistered_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.role})"
