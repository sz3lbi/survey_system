from django.shortcuts import render


def home(request):
    return render(request, "home.html")


def lang(request):
    return render(request, "lang.html")
