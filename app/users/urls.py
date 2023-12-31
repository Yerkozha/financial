from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (AuthViewSet, AppointmentsViewSet)

app_name = "users"

router = DefaultRouter()

router.register("", AuthViewSet)
router.register("appoinments", AppointmentsViewSet, basename='appoinments')

urlpatterns = router.get_urls()