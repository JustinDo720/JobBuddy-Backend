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
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.JobList.as_view(), name='job_list'),
    path('jobs/images/', views.JobImageList.as_view(), name='images_job'),
    path('jobs/images/<int:id>/', views.IndJobImage.as_view(), name='individual_image_job'),
    path('jobs/view/<int:id>/', views.SpecificJob.as_view(), name='specific_job'),
    path('jobs/edit/<int:id>/', views.UpdateJob.as_view(), name='update_job'),
    path('jobs/delete/<int:id>/', views.RemoveJob.as_view(), name='remove_job'),
    # Djoser Configs
    path('activate/<uid>/<token>/', views.redirect_activation_url, name='activate'),
    path('password/reset/confirm/<uid>/<token>/', views.redirect_password_reset_url, name='password_reset'),
    path('username/reset/confirm/<uid>/<token>/', views.redirect_username_reset_url, name='username_reset'),       
]
