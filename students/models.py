from django.db import models

# Create your models here.

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    university = models.CharField(max_length=200)
    course = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
