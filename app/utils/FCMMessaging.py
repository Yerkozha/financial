


# import firebase_admin
from firebase_admin import credentials, messaging

# cred = credentials.Certificate("C:/www/financial/hidjama-3326f-firebase-adminsdk-zr9nh-426699b34c.json")
# firebase_admin.initialize_app(cred)

from firebase_admin.messaging import Message, Notification
from fcm_django.models import FCMDevice


def send_message(title, msg, registartion_token, dataObject=None):
    device = FCMDevice.objects.all()
    device.send_message(Message(notification=Notification(title="title", body="body")))

    # Note: You can also combine the data and notification kwarg
    # FCMDevice.objects.send_message(
    #     Message(notification=Notification(title="title", body="body", image="image_url"))
    # )


    # message = messaging.MulticastMessage(
    #     notification=messaging.Notification(
    #         title=title,
    #         body=msg
    #     ),
    #     data=dataObject,
    #     tokens=registartion_token
    # )
    #
    # response = messaging.send_each_for_multicast(message)
    #
    # print('Successfully delivered ', response)
