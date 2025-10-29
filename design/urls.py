from django.urls import path
from . import views

app_name = 'design'

urlpatterns = [
    path('', views.design_home, name='home'),
]
