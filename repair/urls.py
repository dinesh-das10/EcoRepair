from django.urls import path
from .views import repair_check, process_item_api

urlpatterns = [
    path("check/", repair_check, name="repair-check"),
    path("process/", process_item_api, name="process-item"),
]