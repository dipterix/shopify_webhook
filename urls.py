from django.conf.urls import include, url
from .views import *

urlpatterns = [
  url(r'^product_creation', product_creation),
]