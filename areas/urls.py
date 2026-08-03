from django.urls import path
from . import views

urlpatterns = [
    path("", views.area_list, name="area_list"),
    path("add/", views.add_area, name="add_area"),
    path("<int:area_id>/edit/", views.edit_area, name="edit_area"),
    path("<int:area_id>/delete/", views.delete_area, name="delete_area"),
]