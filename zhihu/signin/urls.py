from django.contrib import admin
from django.urls import path,include
import signin.views

urlpatterns = [
    path(r'index/',signin.views.index),
    path(r'registered/',signin.views.create_user),
    path(r'signin/',signin.views.sign_in)
]