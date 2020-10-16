from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import ChatGrant
from .models import Room


@login_required
def all_rooms(request):
    """"""
    rooms = Room.objects.all()
    return render(request, "rooms.html", {"rooms": rooms})


@login_required
def room_detail(request, slug):
    """"""
    print(slug)
    room = Room.objects.get(slug=slug)
    return render(request, "room.html", {"room": room})


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
def chat(request):
    """"""
    username = request.user.username
    token = AccessToken(
        settings.TWILIO_ACCOUNT_SID,
        settings.TWILIO_API_KEY_SID,
        settings.TWILIO_API_KEY_SECRET,
        identity=username,
    )
    token.add_grant(VideoGrant(room="Chat Room"))

    return render(request, "chat.html", {"token": token.to_jwt().decode()})