from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import Http404

from django.db.models import Q

from .models import Student
from .forms import StudentForm
from users.models import UserProfile

from areas.models import Area
from documents.models import Document

from django.contrib import messages


@login_required
def home(request):
    if request.user.is_superuser:
        total_students = Student.objects.count()
        total_areas = Area.objects.count()
        total_documents = Document.objects.count()
    else:
        try:
            profile = request.user.userprofile

            total_students = Student.objects.filter(
                area=profile.area
            ).count()

            total_areas = 1

            total_documents = Document.objects.filter(
                student__area=profile.area
            ).count()

        except UserProfile.DoesNotExist:
            total_students = 0
            total_areas = 0
            total_documents = 0

    context = {
        "total_students": total_students,
        "total_areas": total_areas,
        "total_documents": total_documents,
    }

    return render(request, "home.html", context)


@login_required
def student_list(request):
    search = request.GET.get("search", "")

    if request.user.is_superuser:
        students = Student.objects.all()
    else:
        try:
            profile = request.user.userprofile
            students = Student.objects.filter(area=profile.area)
        except UserProfile.DoesNotExist:
            students = Student.objects.none()

    if search:
        students = students.filter(
            Q(student_id__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search) |
            Q(university__icontains=search) |
            Q(area__name__icontains=search)
        )

    return render(request, "students.html", {
        "students": students,
        "search": search,
    })


@login_required
def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)

        if form.is_valid():
            student = form.save(commit=False)

            if not request.user.is_superuser:
                profile = request.user.userprofile
                student.area = profile.area

            student.save()
            messages.success(request, "Student added successfully.")
            return redirect("student_list")

    else:
        form = StudentForm()

        if not request.user.is_superuser:
            form.fields["area"].disabled = True

    return render(request, "add_student.html", {
        "form": form
    })


@login_required
def student_detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    if not request.user.is_superuser:
        profile = request.user.userprofile

        if student.area != profile.area:
            raise Http404("Student not found")

    return render(request, "student_detail.html", {
        "student": student
    })


@login_required
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    if not request.user.is_superuser:
        profile = request.user.userprofile

        if student.area != profile.area:
            raise Http404("Student not found")

    if request.method == "POST":
        form = StudentForm(
            request.POST,
            request.FILES,
            instance=student
        )

        if form.is_valid():
            student = form.save(commit=False)

            if not request.user.is_superuser:
                student.area = profile.area

            student.save()
            
            messages.success(request, "Student updated successfully.")

            return redirect("student_detail", student_id=student.id)

    else:
        form = StudentForm(instance=student)

        if not request.user.is_superuser:
            form.fields["area"].disabled = True

    return render(request, "edit_student.html", {
        "form": form,
        "student": student,
    })


@login_required
def delete_student(request, student_id):
    if not request.user.is_superuser:
        raise Http404("Page not found")

    student = get_object_or_404(Student, id=student_id)

    if request.method == "POST":
        student.delete()
        messages.success(request, "Student deleted successfully.")
        return redirect("student_list")

    return render(request, "delete_student.html", {
        "student": student,
    })


def logout_view(request):
    logout(request)
    return redirect("login")