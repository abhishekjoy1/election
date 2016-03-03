from django.conf.urls import url
from . import views
from .views import *

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'^$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', logout_page),
    url(r'^register/$', register),
    url(r'^register/success/$', register_success),
    url(r'^home/$', home),
]