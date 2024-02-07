"""
URL configuration for recommenderforces project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/',     def canBuildSquare(t, test_cases):
        results = []

        for i in range(t):
            n = testCases[i][0]
            squares = testCases[i][1]
            counts = [0] * (max(squares) + 1)
            for square in squares:
                counts[square] += 1
            currentSide = 1
            remainingSquares = n
            possible = True

            while remainingSquares > 0:
                remainingSquares -= currentSide
                currentSide += 1

                if remainingSquares < 0 or counts[currentSide] < remainingSquares:
                    possible = False
                    break

            results.append("YES" if possible else "NO")

        return results

    t = int(input())
    testCases = []

    for i in range(t):
        n = int(input())
        squares = list(map(int, input().split()))
        testCases.append((n, squares))

    results = canBuildSquare(t, test_cases)
    for result in results:
        print(result)

include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', include('problems.urls'))
]
