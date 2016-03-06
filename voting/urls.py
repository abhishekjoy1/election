from django.conf.urls import url, include
from rest_framework import routers
from . import views
from .views import *

router = routers.DefaultRouter()
router.register(r'users', views.CustomUserViewSet)
router.register(r'states', views.StateViewSet)
router.register(r'seats', views.SeatViewSet, base_name="Seat")
router.register(r'booths', views.BoothViewSet, base_name="Booth")


urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'^$', 'django.contrib.auth.views.login'),
    url(r'^api/', include(router.urls)),
    url(r'^logout/$', logout_page),
    url(r'^register/$', register),
    url(r'^register/success/$', register_success),
    url(r'^home/$', home),
]