from django.urls import path
from .views import *
urlpatterns = [
    # Rutas para el modelo Auth
    path('', AuthListView.as_view(), name='auth_list'),
    path('auth/create/', AuthCreateView.as_view(), name='auth_create'),
    path('auth/update/<int:pk>/', AuthUpdateView.as_view(), name='auth_update'),
    path('auth/delete/<int:pk>/', AuthDeleteView.as_view(), name='auth_delete'),
]