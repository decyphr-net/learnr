from django.urls import path
from . import views

urlpatterns = [
    path("", views.modules),
    path("<int:module_id>/", views.lessons),
    path("lesson/<int:lesson_id>", views.units),
    path("unit/<int:unit_id>", views.unit),
]
