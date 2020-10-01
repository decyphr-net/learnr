from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant


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