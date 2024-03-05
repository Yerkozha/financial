"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny

from app.users.views import CustomTokenRefreshView
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from django.conf import settings
from django.conf.urls.static import static

def http_x_accel_redirect(path: str):
    response = ()
    response["Content-Type"] = ""
    response["X-Accel-Redirect"] = path
    return response

@api_view(["GET"])
def media_index(request):
    """Checks permission and read file"""
    path = request.path.replace("/financial/media", "/protected")
    return http_x_accel_redirect(path)

@api_view(["GET"])
@authentication_classes([JWTTokenUserAuthentication, SessionAuthentication])
def media_index_events(request):
    """Checks permission and read file"""
    path = request.path.replace("/financial/media", "/protected")
    return http_x_accel_redirect(path)


@api_view(["GET"])
@permission_classes([AllowAny])
def media_index_external(request):
    """Checks permission and read file"""
    path = request.path.replace("/financial/media", "/protected")
    return http_x_accel_redirect(path)

urlpatterns = [
    re_path(r"^financial/media/events/.+", media_index_events),
    re_path(r"^financial/media/documents/external/.+", media_index_external),
    re_path(r"^financial/media/.+", media_index),

    path('financial/', include('app.financial.urls')),
    path('users/', include('app.users.urls')),
    path('articles/', include('app.articles.urls')),


    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += i18n_patterns(path('admin/', admin.site.urls),)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)