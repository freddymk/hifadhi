from django.shortcuts import render
from .models import Student
from .forms import StudentForm
from django.shortcuts import render, redirect


def home(request):
    total_students = Student.objects.count()
    context = {
        'total_students': total_students,
    }
    return render(request, 'home.html', context)

def student_list(request):
    students = Student.objects.all()

    context = {
        "students": students,
    }

    return render(request, "students.html", context)

def add_student(request):

    if request.method == "POST":
        form = StudentForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("student_list")

    else:
        form = StudentForm()

    return render(request, "add_student.html", {"form": form})

def add_student(request):
    if request.method == "POST":
        student = Student(
            student_id=request.POST["student_id"],
            first_name=request.POST["first_name"],
            last_name=request.POST["last_name"],
            email=request.POST["email"],
            area=request.POST["area"],
        )
        student.save()

        return redirect("/students/")

    return render(request, "add_student.html")

def student_detail(request, student_id):
    student = Student.objects.get(id=student_id)

    context = {
        "student": student,
    }

    return render(request, "student_detail.html", context)