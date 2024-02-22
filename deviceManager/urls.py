from django.contrib import admin
from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from app import views

schema_view = get_schema_view(
   openapi.Info(
      title="Device Manager",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
)

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

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
