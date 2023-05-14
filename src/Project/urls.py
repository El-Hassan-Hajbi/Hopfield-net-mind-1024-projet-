"""
URL configuration for Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from .views import main_page, classify_view, run_model_view, unnoise_view, load_data_view, noise_view


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", main_page),
    path("classify_view/", classify_view, name='classify_view'),
    path("load_data_view/", load_data_view, name='load_data_view'),
    path("unnoise_view/", unnoise_view, name='unnoise_view'),
    path("noise_view/", noise_view, name='noise_view'),
    path("run_model_view/", run_model_view, name='run_model_view'),

]
