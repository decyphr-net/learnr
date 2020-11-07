from django.urls import path
from . import views

urlpatterns = [
    path("", views.chat, name="chat"),
    path("teacher-selection", views.teacher_selection, name="teacher_selection"),
    path("<str:name>", views.classroom, name="classroom"),
    path("token/", views.token, name="token"),
    path("update-conversation/", views.update_conversation, name="update-conversation"),
]
