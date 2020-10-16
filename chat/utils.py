from twilio.jwt.access_token.grants import VideoGrant
from twilio.rest import Client


def get_client():
    """"""
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    return client


def create_conversation(client, name):
    """"""
    return client.conversations.conversations.create(friendly_name=name)


def create_participant(client, sid, identity):
    """"""
    participant = client.conversations.conversations(sid).participants.create(
        identity=identity,
    )