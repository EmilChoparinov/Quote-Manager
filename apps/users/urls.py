from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^(?P<u_id>\d+)/$', views.display_user)
]