from django import forms
from .models import Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "profile_picture",
            "student_id",
            "first_name",
            "last_name",
            "date_of_birth",
            "email",
            "university",
            "course",
            "year_of_study",
            "expected_graduation_date",
            "area",
        ]

        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
            "expected_graduation_date": forms.DateInput(attrs={"type": "date"}),
        }