from django.urls import path
from . import views

urlpatterns = [
    path("recommended/", views.recommended),
    path("rate/", views.rate, name="rate"),
    path("", views.rate),
    path("update_problems", views.update_problems)

]