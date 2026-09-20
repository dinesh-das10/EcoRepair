from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/repair/", include("repair.urls")),
    path("api/collection/", include("collection.urls")),
]