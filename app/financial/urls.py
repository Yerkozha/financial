from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (FinancialViewSet)

app_name = "financial"

router = DefaultRouter()

router.register("", FinancialViewSet, basename='financial')

urlpatterns = router.get_urls()