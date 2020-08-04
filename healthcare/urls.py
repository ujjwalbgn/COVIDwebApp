from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),


    path('', views.home, name="home"),
    path('edit_patient/<str:pk>/', views.editPatient, name="editPatient"),
    path('listpatient/', views.listPatient, name="listPatient"),

    path('testlocation/', views.testLocation, name="testLocation"),
    path('covidscreening/', views.covidScreening, name="covidScreening"),

    path('medication/', views.editMedication, name="medication"),
    path('treatment/', views.editTreatement, name="treatment"),

]
