from django.urls import path
from .views import *
urlpatterns = [
    
    path('device/', DeviceListView.as_view(), name='device_list'),
    path('device/create/', DeviceCreateView.as_view(), name='device_create'),
    path('device/update/<int:pk>/', DeviceUpdateView.as_view(), name='device_update'),
    path('device/delete/<int:pk>/', DeviceDeleteView.as_view(), name='device_delete'),

]