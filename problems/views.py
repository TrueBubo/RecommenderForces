from bisect import bisect_left
from math import ceil
from random import choices

import numpy as np
import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect

from problems.models import Problem
from users.models import Profile

from helper_functions import binary_in, euclidian_distance_squared_per_component, k_smallest_elements


# Shows problems which are recommended based on user ratings
def recommended(request):
    if not request.user.is_authenticated: return redirect("login")
    if request.user.username == "admin": return redirect("/admin")

    # Load user's solved problems
    url = f"https://codeforces.com/api/user.status?handle={request.user}"
    problems = requests.get(url).json()["result"]
    solved_ids = {f"{problem['problem']['contestId']}{problem['problem']['index']}" for problem in problems
                  if 'contestId' in problem['problem'] and 'index' in problem['problem']}

    profile = Profile.objects.get(user=request.user)
    preferences = profile.preferences
    problems = Problem.objects.all()

    # Euclidian distance normalized for number of components
    # Only takes not solved problems which are at most 100 points easier and at most 300 points harder than current standing
    distances = [
        (f"{problem.problem_id} {problem.name}", euclidian_distance_squared_per_component(preferences, problem.tags))
        for problem in problems if
        abs(int(preferences["rating"]) + 100 - int(problem.rating)) < 200 and problem.problem_id not in solved_ids]
    # Takes 1000 closest problems
    k = 1000
    closest_problems = k_smallest_elements(distances, min(k, len(distances) - 1))
    # numpy will normalize it to sum to 1
    probability_function = np.arange(min(k, len(distances)) - 1, 0, -1)
    chosen_problems = choices(closest_problems, probability_function, k=20)

    chosen_problems_info = []
    for problem in chosen_problems:
        id, name = problem[0].split(" ", 1)
        for idx in range(len(id)):
            if id[idx].isalpha():
                contest = id[:idx]
                index = id[idx:]
        chosen_problems_info.append((name, contest, index))

    return render(request, "recommended.html", {"problems": chosen_problems_info})


# Shows problem which are yet to be rated
def rate(request):
    if not request.user.is_authenticated: return redirect("login")
    if request.user.username == "admin": return redirect("/admin")

    # Updates db with new ratings
    if request.method == "POST":
        profile = Profile.objects.get(user=request.user)
        preferences = profile.preferences
        rated_problems = profile.rated_problems
        for problem_id in request.POST:
            user_rating = request.POST[problem_id]
            if user_rating != '0' and problem_id != "csrfmiddlewaretoken":  # Was rating and is a problem
                user_rating = int(user_rating)
                try:
                    problem = Problem.objects.get(problem_id=problem_id)
                except:  # Db was out of date
                    update_problems(request)
                    problem = Problem.objects.get(problem_id=problem_id)
                tags = problem.tags
                rating = problem.rating

                # Average of ratings of problems
                preferences["rating"] = ceil(
                    (preferences.get("rating", 0) * len(rated_problems) + rating) / (len(rated_problems) + 1))

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
        if not "contestId" in problemInfo or not "index" in problemInfo: continue  # Problem does not have valid identificators
        problemId = f"{problemInfo['contestId']}{problemInfo['index']}"
        if problemId not in unique_ids and not binary_in(rated_problems, problemId):
            unique_ids.add(problemId)
            problems_names.append((f"{problemInfo['contestId']}{problemInfo['index']}", problemInfo['name']))
    return render(request, "rate.html", {"problems": problems_names})


def update_problems(request):
    if not request.user.is_authenticated: return redirect("login")
    if request.user.username == "admin": return redirect("/admin")

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
