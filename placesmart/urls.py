"""
URL configuration for placesmart project.

The `urlpatterns` list routes URLs to views. 
For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path
from user import views  # Importing our app's views

urlpatterns = [
    path('admin/', admin.site.urls),          # Django admin page
    path('signup/', views.signup_view, name='signup'),  # Signup page
    path('login/', views.login_view, name='login'),     # Login page
    path('', views.home_view, name='home'),             # Home page (default)
    path('logout/', views.logout_view, name='logout'),  # Logout action
    path('aptitude/', views.aptitudetest_view, name='aptitudetest'),
    path('selection_page/', views.selection_page, name='selection_page'),
    path('QuantitativeAbility/', views.ap_test1_view, name='ap_test1'),
    path('LogicalReasoning/', views.ap_test2_view, name='ap_test2'),
    path("Grammer", views.ap_test3_view, name="ap_test3"),


]
