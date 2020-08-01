from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name="home"),
    path('edit_pateint/<str:pk>/', views.editPateint, name="editPateint"),
]
