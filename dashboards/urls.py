from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('pandhar-raste/', views.pandhar_raste_dashboard, name='pandhar_raste'),
    path('e-haqq/', views.e_haqq_dashboard, name='e_haqq'),
    path('e-ferfar/', views.e_ferfar_dashboard, name='e_ferfar'),
    path('e-ferfar-2/', views.e_ferfar_2_dashboard, name='e_ferfar_2'),
    path('e-chavdi/', views.e_chavdi_dashboard, name='e_chavdi'),
    path('agristack/', views.agristack_dashboard, name='agristack'),
]
