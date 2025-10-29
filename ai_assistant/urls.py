from django.urls import path
from . import views

app_name = 'ai_assistant'

urlpatterns = [
    path('', views.ai_chat, name='ai_chat'),
    path('commands/', views.ai_commands, name='ai_commands'),
    path('api/chat/', views.chat_message, name='chat_message'),
    path('api/status/', views.ai_status, name='ai_status'),
]
