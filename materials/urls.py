from django.urls import path
from . import views

app_name = 'materials'

urlpatterns = [
    path('', views.materials_home, name='home'),
    path('catalog/', views.material_catalog, name='catalog'),
    path('material/<int:material_id>/', views.material_detail, name='material_detail'),
    path('suppliers/', views.supplier_directory, name='supplier_directory'),
    path('calculator/', views.cost_calculator, name='cost_calculator'),
    path('estimates/', views.my_estimates, name='my_estimates'),
    path('estimates/create/', views.create_estimate, name='create_estimate'),
    path('estimates/<int:estimate_id>/', views.estimate_detail, name='estimate_detail'),
    
    # API endpoints
    path('api/calculate/', views.calculate_materials, name='api_calculate'),
    path('api/add-item/', views.add_estimate_item, name='api_add_item'),
    path('api/price-comparison/', views.price_comparison, name='api_price_comparison'),
    path('api/search/', views.material_search, name='api_search'),
]
