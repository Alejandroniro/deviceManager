from django.contrib import admin
from django.urls import path

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

    path('device_execution/', views.device_execution_list, name='device_execution_list'),
    path('device_execution/<int:device_execution_id>/', views.device_execution_detail, name='device_execution_detail'),
    path('device_execution/<int:device_id>/ping/', views.device_execution_ping, name='device_execution_ping'),
]
