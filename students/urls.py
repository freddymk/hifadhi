from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    # Student list
    path("students/", views.student_list, name="student_list"),

    # Add student
    path("students/add/", views.add_student, name="add_student"),

    # Student profile
    path("students/<int:student_id>/", views.student_detail, name="student_detail"),
    path("students/<int:student_id>/edit/", views.edit_student, name="edit_student"),
    path("students/<int:student_id>/delete/", views.delete_student, name="delete_student"),
]