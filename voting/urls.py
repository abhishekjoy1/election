from django.conf.urls import url, include
from rest_framework import routers
from . import views
from .views import *
from django.contrib import admin
admin.autodiscover()
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
    url(r'^vote/$', vote),
    url(r'^update_election_status/$', update_election_status),
    url(r'^count_vote/$', count_vote),
    url(r'^result_count/(?P<level>state|seat|country)/(?P<id>\d+)$', result_count),
    url(r'^add_state/$', add_state),
    url(r'^add_seat/$', add_seat),
    url(r'^add_booth/$', add_booth),
    url(r'^admin/', include(admin.site.urls)),
]