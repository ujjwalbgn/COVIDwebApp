from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),


    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="healthcare/password_reset.html"),
         name="reset_password"),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="healthcare/password_reset_sent.html"),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="healthcare/password_reset_form.html"),
         name="password_reset_confirm"),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="healthcare/password_reset_done.html"),
         name="password_reset_complete"),

    path('', views.home, name="home"),
    path('edit_patient/<str:pk>/', views.editPatient, name="editPatient"),
    path('listpatient/', views.listPatient, name="listPatient"),

    path('testlocation/', views.testLocation, name="testLocation"),
    path('covidscreening/', views.covidScreening, name="covidScreening"),

    path('medication/', views.editMedication, name="medication"),
    path('treatment/', views.editTreatement, name="treatment"),

    path('assign_med/', views.assignMed, name="assignMed"),
    path('assign_treatment/', views.assignTreatment, name="assignTreatment"),

    path('deletepatient/<str:pk>/', views.DeletePatient, name="deletepatient"),
]
