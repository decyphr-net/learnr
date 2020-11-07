from django.conf import settings
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import ChatGrant
from twilio.jwt.access_token.grants import VideoGrant


def get_twilio_token(username, classroom_name):
    token = AccessToken(
        settings.TWILIO_ACCOUNT_SID,
        settings.TWILIO_API_KEY_SID,
        settings.TWILIO_API_KEY_SECRET,
        identity=username,
    )

    token.add_grant(VideoGrant(room=classroom_name))
    return token.to_jwt().decode()