from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="activities_dashboard"),
]
