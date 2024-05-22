from django.urls import path
from . import views

urlpatterns = [
    path('api_request/', views.api_request_view, name='api_request'),
]
