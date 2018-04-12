from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from api import views


router = routers.DefaultRouter()
router.register(r'shipments', views.ShipmentViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'cities', views.CityViewSet)
router.register(r'streets', views.StreetViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),

    path('admin/', admin.site.urls),
    url(r'^auth/token/obtain/$', obtain_jwt_token),
    url(r'^auth/token/refresh/$', refresh_jwt_token),
    url(r'^auth/token/verify/$', verify_jwt_token),
]
