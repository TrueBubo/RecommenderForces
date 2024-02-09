from django.urls import path
from . import views

urlpatterns = [
    path("problems/", views.get_problems, name="all_problems"),
    path("update/", views.update_problems, name="update"),
    path("completedProblems/<str:user>/", views.get_user_problems, name="get_user_problems")
]