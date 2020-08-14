"""helpdesk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from hd.views import ClaimViewSet
from users.views import UserViewSet, ObtainTokenView


router = routers.DefaultRouter()
router.register(r'claims', ClaimViewSet, basename='ClaimModel')
router.register(r'users', UserViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('obtain_token/', ObtainTokenView.as_view()),
    path('admin/', admin.site.urls),
    path('', include('hd.urls')),
    path('users/', include('users.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
