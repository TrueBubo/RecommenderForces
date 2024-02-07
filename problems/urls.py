from django.urls import path
from . import views

urlpatterns = [
    path("hello/", views.say_name),
    path("recommended/", views.recommended),
    path("rate/", views.rate),
    path("", views.rate),
    path("update_problems", views.update_problems)
]