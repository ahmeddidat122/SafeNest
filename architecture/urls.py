from django.urls import path
from . import views

app_name = 'architecture'

urlpatterns = [
    path('', views.architecture_home, name='home'),
    path('generator/', views.ai_generator, name='ai_generator'),
    path('gallery/', views.project_gallery, name='project_gallery'),
    path('create/', views.create_project, name='create_project'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('project/<int:project_id>/generate/', views.generate_model, name='generate_model'),
    path('project/<int:project_id>/share/', views.share_project, name='share_project'),
    
    # API endpoints
    path('api/generate/', views.generate_architecture_ai, name='api_generate'),
    path('api/estimate-materials/', views.estimate_materials, name='api_estimate_materials'),
    path('api/progress/<int:project_id>/', views.generation_progress, name='api_progress'),
]
