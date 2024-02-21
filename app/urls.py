from django.urls import path
from .views import *
urlpatterns = [
    # Rutas para el modelo Auth
    path('', AuthListView.as_view(), name='auth_list'),
    path('auth/create/', AuthCreateView.as_view(), name='auth_create'),
    path('auth/update/<int:pk>/', AuthUpdateView.as_view(), name='auth_update'),
    path('auth/delete/<int:pk>/', AuthDeleteView.as_view(), name='auth_delete'),

    # Rutas para el modelo Device
    path('device/', DeviceListView.as_view(), name='device_list'),
    path('device/create/', DeviceCreateView.as_view(), name='device_create'),
    path('device/update/<int:pk>/', DeviceUpdateView.as_view(), name='device_update'),
    path('device/delete/<int:pk>/', DeviceDeleteView.as_view(), name='device_delete'),

    # Rutas para el modelo DeviceExecution
    path('deviceexecution/', DeviceExecutionListView.as_view(), name='deviceexecution_list'),
    path('deviceexecution/create/', DeviceExecutionCreateView.as_view(), name='deviceexecution_create'),
    path('deviceexecution/update/<int:pk>/', DeviceExecutionUpdateView.as_view(), name='deviceexecution_update'),
    path('deviceexecution/delete/<int:pk>/', DeviceExecutionDeleteView.as_view(), name='deviceexecution_delete'),
]