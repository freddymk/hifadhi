from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm


def home(request):
    total_students = Student.objects.count()

    context = {
        "total_students": total_students,
    }

    return render(request, "home.html", context)


def student_list(request):
    students = Student.objects.all()

    context = {
        "students": students,
    }

    return render(request, "students.html", context)


def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("student_list")

    else:
        form = StudentForm()

    return render(request, "add_student.html", {
        "form": form
    })


def student_detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    return render(request, "student_detail.html", {
        "student": student
    })


def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    if request.method == "POST":
        form = StudentForm(
            request.POST,
            request.FILES,
            instance=student
        )

        if form.is_valid():
            form.save()
            return redirect("student_detail", student_id=student.id)

    else:
        form = StudentForm(instance=student)

    return render(request, "edit_student.html", {
        "form": form,
        "student": student,
    })


def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    if request.method == "POST":
        student.delete()
        return redirect("student_list")

    return render(request, "delete_student.html", {
        "student": student,
    })