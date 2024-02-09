from math import ceil

from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
from rest_framework.response import Response
from problems.models import Problem
from users.models import Profile
from bisect import bisect_left

def binary_search(a, x):
    i = bisect_left(a, x)
    if i != len(a) and a[i] == x:
        return True
    else:
        return False

def get_problems(request):
    response = requests.get("https://codeforces.com/api/problemset.problems").json()
    return Response(response)


def recommended(request):
    if not request.user.is_authenticated: return redirect("login")
    return render(request, "recommended.html", {})


def rate(request):
    if not request.user.is_authenticated: return redirect("login")

    if request.method == "POST":
        profile = Profile.objects.get(user=request.user)
        preferences = profile.preferences
        rated_problems = profile.rated_problems
        for problem_id in request.POST:
            user_rating = request.POST[problem_id]
            if user_rating != '0' and problem_id != "csrfmiddlewaretoken": # Was rating and is a problem
                user_rating = int(user_rating)
                problem = Problem.objects.get(problem_id=problem_id)
                tags = problem.tags
                rating = problem.rating

                # Average of ratings of problems
                preferences["rating"] = ceil((preferences.get("rating", 0) * len(rated_problems) + rating) / (len(rated_problems) + 1))

                for tag in tags:
                    preferences[tag] = preferences.get(tag, [0, 0])
                    preferences[tag][0] += user_rating
                    preferences[tag][1] += 1

                rated_problems.append(problem_id)
        profile.rated_problems = sorted(rated_problems)
        profile.preferences = preferences
        profile.save()

    # Load user's solved problems
    url = f"https://codeforces.com/api/user.status?handle={request.user}"
    problems = requests.get(url).json()["result"]
    problems_names = []
    unique_ids = set()

    # Get already rated problems to avoid duplicate rating
    rated_problems = Profile.objects.get(user=request.user).rated_problems


    # Only get problemID + name
    for problem in problems:
        problemInfo = problem['problem']
        problemId = f"{problemInfo['contestId']}{problemInfo['index']}"
        if problemId not in unique_ids and not binary_search(rated_problems, problemId):
            unique_ids.add(problemId)
            problems_names.append((f"{problemInfo['contestId']}{problemInfo['index']}", problemInfo['name']))
    return render(request, "rate.html", {"problems": problems_names})


def update_problems(request):
    if not request.user.is_authenticated: return redirect("login")

    # Load all problems
    url = "https://codeforces.com/api/problemset.problems"
    response = requests.get(url).json()["result"]["problems"]

    # Save new problems to db
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
