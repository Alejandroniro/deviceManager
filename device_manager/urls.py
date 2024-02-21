from django.urls import path
from .views import *
urlpatterns = [
   # Rutas para el modelo DeviceExecution
    path('deviceexecution/', DeviceExecutionListView.as_view(), name='deviceexecution_list'),
    path('deviceexecution/create/', DeviceExecutionCreateView.as_view(), name='deviceexecution_create'),
    path('deviceexecution/update/<int:pk>/', DeviceExecutionUpdateView.as_view(), name='deviceexecution_update'),
    path('deviceexecution/delete/<int:pk>/', DeviceExecutionDeleteView.as_view(), name='deviceexecution_delete'),
]