""" URL mapping for the USER API"""
from django.urls import path

from user import views


app_name = 'user'

urlpatterns = [
    path('create/', view=views.CrateUserView.as_view(), name="create")
]
