from rest_framework.routers import DefaultRouter
from .views import ArticlesViewSet

app_name = "articles"

router = DefaultRouter()

router.register("", ArticlesViewSet)
# router.register("appoinments", AppointmentsViewSet, basename='appoinments')
# router.register("", DeviceTokenViewSet, basename='device_token')


urlpatterns = router.get_urls()
