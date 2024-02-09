from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
from rest_framework.response import Response
from problems.models import Problem


def get_problems(request):
    response = requests.get("https://codeforces.com/api/problemset.problems").json()
    return Response(response)


def recommended(request):
    if not request.user.is_authenticated: return redirect("login")
    return render(request, "recommended.html", {})


def rate(request):
    if not request.user.is_authenticated: return redirect("login")
    url = f"https://codeforces.com/api/user.status?handle={request.user}"
    problems = requests.get(url).json()["result"]
    problems_names = []
    unique_ids = set()
    for problem in problems:
        problemInfo = problem['problem']
        problemId = f"{problemInfo['contestId']}{problemInfo['index']}"
        if problemId not in unique_ids:
            unique_ids.add(problemId)
            problems_names.append((f"{problemInfo['contestId']}{problemInfo['index']}", problemInfo['name']))
    return render(request, "rate.html", {"problems": problems_names})


def update_problems(request):
    if not request.user.is_authenticated: return redirect("login")
    url = "https://codeforces.com/api/problemset.problems"
    response = requests.get(url).json()["result"]["problems"]

    for problem_data in response:
        problem_id = str(problem_data["contestId"]) + problem_data["index"]
        name = problem_data["name"]
        rating = problem_data.get("rating", None)  # Some problems may not have a rating
        tags = problem_data.get("tags", [])
        if rating is None: continue
        if Problem.objects.filter(problem_id=problem_id).first() is None:  # Would be unique
            problem = Problem(
                problem_id=problem_id,
                name=name,
                rating=rating,
                tags=tags
            )
            problem.save()
        else:
            break
    return HttpResponse("""<html><script>window.location.replace('/');</script></html>""")
