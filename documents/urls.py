from django.urls import path
from . import views

urlpatterns = [
    path(
        "student/<int:student_id>/upload/",
        views.upload_document,
        name="upload_document",
    ),
]