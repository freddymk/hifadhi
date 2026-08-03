from django.db import models
from students.models import Student
from django.contrib.auth.models import User


class Document(models.Model):

    DOCUMENT_TYPES = [
        ("MOA", "MOA"),
        ("PAYMENT_RECEIPT", "Payment Receipt"),
        ("MONITORING", "Monitoring & Evaluation Template"),
        ("FINANCIAL_PLAN", "Student Financial Plan Book"),
        ("COURSE_COMPLETION", "Course Completion Document"),
        ("EXAM_RESULTS", "Exam Results"),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="documents"
    )

    document_type = models.CharField(
        max_length=50,
        choices=DOCUMENT_TYPES
    )

    file = models.FileField(
        upload_to="documents/"
    )

    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.student} - {self.document_type}"