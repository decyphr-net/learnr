from django.urls import path
from . import views

urlpatterns = [
    path("", views.chat, name="chat"),
    path("rooms", views.all_rooms, name="all_rooms"),
    path("rooms/<str:slug>", views.room_detail, name="room_detail"),
    path("token/", views.token, name="token"),
]
