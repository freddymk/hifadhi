from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404

from students.models import Student
from users.models import UserProfile

from .models import Document
from .forms import DocumentForm


@login_required
def upload_document(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    # Area Admin can only access students in their own area
    if not request.user.is_superuser:
        profile = request.user.userprofile

        if student.area != profile.area:
            raise Http404("Student not found")

    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():

            document_type = form.cleaned_data["document_type"]

            existing = Document.objects.filter(
                student=student,
                document_type=document_type
            ).first()

            if existing:
                existing.file.delete(save=False)
                existing.file = form.cleaned_data["file"]
                existing.uploaded_by = request.user
                existing.save()

                messages.success(request, "Document updated successfully.")

            else:
                document = form.save(commit=False)
                document.student = student
                document.uploaded_by = request.user
                document.save()

                messages.success(request, "Document uploaded successfully.")

            return redirect("student_detail", student_id=student.id)

    else:
        form = DocumentForm()

    return render(
        request,
        "documents/upload_document.html",
        {
            "form": form,
            "student": student,
        },
    )