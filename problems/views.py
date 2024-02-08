from django.shortcuts import render
from django.http import HttpResponse
import requests
from rest_framework.response import Response
from problems.models import Problem

def get_problems(request):
    response = requests.get("https://codeforces.com/api/problemset.problems").json()
    return Response(response)

def recommended(request):
    return render(request, "recommended.html", {})

def rate(request):
    return render(request, "rate.html", {"request": request})

def update_problems(request):
    url = "https://codeforces.com/api/problemset.problems"
    response = requests.get(url).json()["result"]["problems"]

    for problem_data in response:
        problem_id = str(problem_data["contestId"]) + problem_data["index"]
        name = problem_data["name"]
        rating = problem_data.get("rating", None)  # Some problems may not have a rating
        tags = problem_data.get("tags", [])
        if rating is None: continue
        if Problem.objects.filter(problem_id=problem_id).first() is None: # Would be unique
            problem = Problem(
                problem_id=problem_id,
                name=name,
                rating=rating,
                tags=tags
            )
            problem.save()
        else: break
    return HttpResponse("""<html><script>window.location.replace('/');</script></html>""")
