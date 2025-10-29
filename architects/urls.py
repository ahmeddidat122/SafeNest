from django.urls import path
from . import views

app_name = 'architects'

urlpatterns = [
    path('', views.architect_directory, name='directory'),
    path('profile/<int:architect_id>/', views.architect_profile, name='profile'),
    path('profile/<int:architect_id>/portfolio/<int:portfolio_id>/', views.architect_portfolio_detail, name='portfolio_detail'),
    path('profile/<int:architect_id>/inquiry/', views.send_inquiry, name='send_inquiry'),
    path('profile/<int:architect_id>/review/', views.submit_review, name='submit_review'),
    path('dashboard/', views.architect_dashboard, name='dashboard'),
    
    # API endpoints
    path('api/search/', views.search_architects, name='api_search'),
    path('api/quick-inquiry/', views.quick_inquiry, name='api_quick_inquiry'),
    path('api/stats/', views.architect_stats, name='api_stats'),
]
