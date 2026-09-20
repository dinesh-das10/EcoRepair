from django.urls import path
from .views import find_center

urlpatterns = [
    path("nearest/", find_center, name="nearest-center"),
]