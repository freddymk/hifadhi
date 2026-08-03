from django.db import models
from areas.models import Area


class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    date_of_birth = models.DateField(
        null=True,
        blank=True
    )

    email = models.EmailField()

    university = models.CharField(
        max_length=200,
        blank=True
    )

    course = models.CharField(
        max_length=200,
        blank=True
    )

    year_of_study = models.CharField(
        max_length=50,
        blank=True
    )

    expected_graduation_date = models.DateField(
        null=True,
        blank=True
    )

    area = models.ForeignKey(
        Area,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    profile_picture = models.ImageField(
        upload_to="students/",
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"