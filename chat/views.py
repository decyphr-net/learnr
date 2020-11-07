import json
from datetime import date
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Classroom, Conversation
from .helpers.twilio import get_twilio_token


@login_required
def teacher_selection(request):
    """"""
    return render(request, "teacher-selection.html")


@login_required
def classroom(request, name):
    """"""
    host = User.objects.get(username=name)
    student = request.user
    classroom_name = f"{host.username} and {student.username} - {date.today()}"
    token = get_twilio_token(student.username, classroom_name)

    classroom, created = Classroom.objects.get_or_create(
        name=classroom_name,
        defaults={
            "description": classroom_name,
            "slug": f"{date.today}",
            "host": host,
            "student": student,
        },
    )
    return render(
        request,
        "classroom.html",
        {"classroom": classroom, "token": token},
    )


@login_required
def token(request):
    """"""
    identity = request.GET.get("identity", request.user.username)
    device_id = request.GET.get("device", "default")

    account_sid = settings.TWILIO_ACCOUNT_SID
    api_key = settings.TWILIO_API_KEY_SID
    api_secret = settings.TWILIO_API_KEY_SECRET
    chat_service_sid = settings.TWILIO_CHAT_SERVER_SID

    token = AccessToken(account_sid, api_key, api_secret, identity=identity)

    endpoint = "MyDjangoChatRoom:{0}:{1}".format(identity, device_id)

    if chat_service_sid:
        chat_grant = ChatGrant(endpoint_id=endpoint, service_sid=chat_service_sid)
        token.add_grant(chat_grant)

    response = {"identity": identity, "token": token.to_jwt().decode("utf-8")}

    return JsonResponse(response)


@login_required
def update_conversation(request):
    data = json.loads(request.body)
    classroom = Classroom.objects.get(name=data["room"])

    conversation = Conversation(
        room=classroom, sender=request.user, message=data["message"]
    )
    conversation.save()
    return JsonResponse({"message": "created"}, status=201)