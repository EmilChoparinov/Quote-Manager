from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.display_quotes),
    url(r'^add_quote$', views.add_quote),
    url(r'^(?P<q_id>\d+)/fav$', views.add_to_fav),
    url(r'^(?P<q_id>\d+)/unfav$', views.remove_from_fav)
]