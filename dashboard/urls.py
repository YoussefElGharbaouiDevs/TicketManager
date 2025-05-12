from django.urls import path
from . import views

urlpatterns = [
path('dashboard/', views.agent_stats_dashboard, name='agent_stats_dashboard'),
]