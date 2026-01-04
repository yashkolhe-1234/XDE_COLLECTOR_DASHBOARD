from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('pandhar-raste/', views.pandhar_raste_dashboard, name='pandhar_raste'),
    # Static management routes must come BEFORE the dynamic taluka route
    path('pandhar-raste/manage/', views.pandhar_raste_manage, name='pandhar_raste_manage'),
    path('pandhar-raste/manage/add/', views.pandhar_raste_add, name='pandhar_raste_add'),
    path('pandhar-raste/manage/edit/<int:pk>/', views.pandhar_raste_edit, name='pandhar_raste_edit'),
    path('pandhar-raste/manage/delete/<int:pk>/', views.pandhar_raste_delete, name='pandhar_raste_delete'),
    path('pandhar-raste/manage/import/', views.pandhar_raste_import, name='pandhar_raste_import'),
    # Dynamic taluka route must come AFTER all static routes
    path('pandhar-raste/<str:taluka>/', views.pandhar_raste_detail, name='pandhar_raste_detail'),
    path('e-haqq/', views.e_haqq_dashboard, name='e_haqq'),
    path('e-ferfar/', views.e_ferfar_dashboard, name='e_ferfar'),
    path('e-ferfar-2/', views.e_ferfar_2_dashboard, name='e_ferfar_2'),
    path('e-chavdi/', views.e_chavdi_dashboard, name='e_chavdi'),
    path('agristack/', views.agristack_dashboard, name='agristack'),
]
