from django.urls import path
from . import views


urlpatterns = [
    path('', views.sign_in),
    path('sign-in', views.sign_in),
    path('sign-up', views.sign_up)
]
