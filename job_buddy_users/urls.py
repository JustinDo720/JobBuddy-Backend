"""
URL configuration for job_buddy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path,include
from . import views

app_name = 'job_buddy_users'  # This is crucial for namespacing
urlpatterns = [
    path('api/token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('api-auth/', include('rest_framework.urls')),
    path('all/', views.JobUsers.as_view(), name='all_users'),
    path('jobs/', views.UserSpecificJobs.as_view(), name='all_users_job'),
    path('details/<int:id>/', views.SpecificUser.as_view(), name='specific_user'),
    path('details/<int:id>/jobs/', views.SpecificUserJobs.as_view(), name='specific_user_jobs')
]
