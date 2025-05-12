from django.urls import path
from . import views

urlpatterns = [
    path('', views.ticket_list, name='ticket_list'),
    path('create/', views.ticket_create, name='ticket_create'),
    path('<int:pk>/', views.ticket_detail, name='ticket_detail'),
    path('dashboard/', views.agent_dashboard, name='agent_dashboard'),
    path('dashboard/item/<int:pk>/', views.ticket_detail_edit, name='ticket_detail_edit'),
    path('tickets/<int:ticket_id>/close/', views.close_ticket, name='close_ticket'),

]
