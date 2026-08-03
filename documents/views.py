from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from students.models import Student
from .models import Document
from .forms import DocumentForm


@login_required
def upload_document(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            document = form.save(commit=False)
            document.student = student
            document.uploaded_by = request.user
            document.save()

            return redirect("student_detail", student_id=student.id)

    else:
        form = DocumentForm()

    return render(request, "documents/upload_document.html", {
        "form": form,
        "student": student,
    })