from django.urls import path
from . import views

app_name = 'consultation'

urlpatterns = [
    path('', views.consultation_home, name='home'),
    path('consultants/', views.find_consultants, name='find_consultants'),
    path('consultant/<int:consultant_id>/', views.consultant_profile, name='consultant_profile'),
    path('request/', views.request_consultation, name='request_consultation'),
    path('request/<int:consultant_id>/', views.request_consultation, name='request_consultation_with_consultant'),
    path('my-consultations/', views.my_consultations, name='my_consultations'),
    path('my-requests/', views.my_requests, name='my_requests'),
    path('session/<int:session_id>/chat/', views.chat_session, name='chat_session'),
    path('session/<int:session_id>/feedback/', views.session_feedback, name='session_feedback'),
    
    # API endpoints
    path('api/send-message/', views.send_message, name='api_send_message'),
    path('api/messages/<int:session_id>/', views.get_messages, name='api_get_messages'),
    path('api/start-session/', views.start_session, name='api_start_session'),
    path('api/end-session/', views.end_session, name='api_end_session'),
]
