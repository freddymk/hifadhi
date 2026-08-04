from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404

from .models import Area
from .forms import AreaForm
from users.models import UserProfile


@login_required
def area_list(request):
    if request.user.is_superuser:
        areas = Area.objects.all()
    else:
        try:
            profile = request.user.userprofile
            areas = Area.objects.filter(id=profile.area.id)
        except UserProfile.DoesNotExist:
            areas = Area.objects.none()

    return render(request, "areas/area_list.html", {
        "areas": areas,
    })


@login_required
def add_area(request):
    if not request.user.is_superuser:
        raise Http404("Page not found")

    if request.method == "POST":
        form = AreaForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, "Area created successfully.")

            return redirect("area_list")

    else:
        form = AreaForm()

    return render(request, "areas/add_area.html", {
        "form": form,
    })


@login_required
def edit_area(request, area_id):
    if not request.user.is_superuser:
        raise Http404("Page not found")

    area = get_object_or_404(Area, id=area_id)

    if request.method == "POST":
        form = AreaForm(request.POST, instance=area)

        if form.is_valid():
            form.save()

            messages.success(request, "Area updated successfully.")

            return redirect("area_list")

    else:
        form = AreaForm(instance=area)

    return render(request, "areas/edit_area.html", {
        "form": form,
        "area": area,
    })


@login_required
def delete_area(request, area_id):
    if not request.user.is_superuser:
        raise Http404("Page not found")

    area = get_object_or_404(Area, id=area_id)

    if request.method == "POST":
        area.delete()

        messages.success(request, "Area deleted successfully.")

        return redirect("area_list")

    return render(request, "areas/delete_area.html", {
        "area": area,
    })