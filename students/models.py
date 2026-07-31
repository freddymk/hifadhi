from django.db import models

# Create your models here.

class Student(models.Model):
    student_id = models.CharField(max_length=20)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    area = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
