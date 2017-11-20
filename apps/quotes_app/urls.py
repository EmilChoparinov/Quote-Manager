from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.display_quotes),
    url(r'^add_quote$', views.add_quote)
]