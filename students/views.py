from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import Http404

from .models import Student
from .forms import StudentForm
from users.models import UserProfile


@login_required
def home(request):
    if request.user.is_superuser:
        total_students = Student.objects.count()
    else:
        try:
            profile = request.user.userprofile
            total_students = Student.objects.filter(area=profile.area).count()
        except UserProfile.DoesNotExist:
            total_students = 0

    context = {
        "total_students": total_students,
    }

    return render(request, "home.html", context)


@login_required
def student_list(request):
    if request.user.is_superuser:
        students = Student.objects.all()
    else:
        try:
            profile = request.user.userprofile
            students = Student.objects.filter(area=profile.area)
        except UserProfile.DoesNotExist:
            students = Student.objects.none()

    return render(request, "students.html", {
        "students": students,
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
        return redirect("student_list")

    return render(request, "delete_student.html", {
        "student": student,
    })


def logout_view(request):
    logout(request)
    return redirect("login")