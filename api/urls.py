from django.urls import path
from . import views

urlpatterns = [
    path("problems/", views.get_problems),
    path("update/", views.update_problems)
]