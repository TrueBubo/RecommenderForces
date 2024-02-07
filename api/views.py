from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from problems.models import Problem
import requests
@api_view(["GET"])
def get_problems(request):
    all_problems = Problem.objects.all()

    problems_serialized = []
    for problem in all_problems:
        problems_serialized.append({"id": problem.problem_id, "name": problem.name, "rating": problem.rating, "tags": problem.tags})
    return JsonResponse(problems_serialized, safe=False)

@api_view(["GET"])
def update_problems(request):
    url = "https://codeforces.com/api/problemset.problems"
    response = requests.get(url).json()["result"]["problems"]

    return Response(response)
