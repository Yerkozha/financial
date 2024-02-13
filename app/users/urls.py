from django.urls import path, re_path
from rest_framework.routers import DefaultRouter

from .views import (AuthViewSet, AppointmentsViewSet, DeviceTokenViewSet)
from fcm_django.api.rest_framework import FCMDeviceViewSet
from . import consumers

app_name = "users"

router = DefaultRouter()

router.register("", AuthViewSet)
router.register("appoinments", AppointmentsViewSet, basename='appoinments')
router.register("", DeviceTokenViewSet, basename='device_token')

router.register('devices', FCMDeviceViewSet)

urlpatterns = router.get_urls()


websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
]