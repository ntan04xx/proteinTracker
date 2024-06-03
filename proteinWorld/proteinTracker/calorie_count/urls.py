from django.urls import path
from . import views

urlpatterns = [
    path('api_request/', views.api_request_view, name='api_request'),
    path('', views.home_page, name = "home"),
    path('target_request/', views.target_request_view, name = "target_request")
]
