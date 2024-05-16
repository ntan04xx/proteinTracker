from django.urls import path
from . import views

urlpatterns = [
    path('count/', views.getCalories, name = "Calorie Calculator"),
]
