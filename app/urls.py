from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.person_create_view, name='create_person'),
    path('', views.welcome, name='welcome'),
    path('reset/', views.person_create_reset_view, name='create_person_reset'),
    path('success/', views.person_create_view, name='success_page'),
    path('persons/', views.payroll_employee_list, name='person_list'),# Add a success page or redirect
    path('persons_reset/', views.payroll_employee_list_reset, name='person_list_reset'),# Add a success page or redirect
    path('update-status/<int:check_number>/', views.update_status, name='update_status'),
    path('update-status-reset/<int:check_number>/', views.update_status_reset, name='update_status_reset'),
]
