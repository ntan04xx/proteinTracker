from django.shortcuts import render
from django.http import HttpResponse


def getCalories(request):
    return HttpResponse("Food")
