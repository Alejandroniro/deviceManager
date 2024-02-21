"""deviceManager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import include, path
from authentication import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("signup/", views.signup, name='signup'),
    path("signin/", views.signin, name="signin"),

    path('device/', views.device_list, name='device_list'),
    path('device/<int:device_id>/', views.device_detail, name='device_detail'),
    path('device/create/', views.device_create, name='device_create'),
    path('device/<int:device_id>/update/', views.device_update, name='device_update'),
    path('device/<int:device_id>/delete/', views.device_delete, name='device_delete'),

    path('device_manager/', views.device_manager_list, name='device_manager_list'),
    path('device_manager/<int:device_manager_id>/', views.device_manager_detail, name='device_manager_detail'),
    path('device_manager/<int:device_id>/ping/', views.device_manager_ping, name='device_manager_ping'),
    path('device_manager/<int:device_manager_id>/delete/', views.device_manager_delete, name='device_manager_delete'),

]
