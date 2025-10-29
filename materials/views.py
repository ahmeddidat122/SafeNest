from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Avg
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import (
    MaterialCategory, Material, Supplier, SupplierMaterial,
    ProjectEstimate, EstimateItem, PriceHistory, MaterialCalculator
)
import json

def materials_home(request):
    """Materials and cost estimation home page"""
    categories = MaterialCategory.objects.all()
    featured_materials = Material.objects.filter(is_available=True)[:8]
    top_suppliers = Supplier.objects.filter(is_active=True, is_verified=True)[:6]
    
    context = {
        'title': 'Materials & Cost Estimation',
        'categories': categories,
        'featured_materials': featured_materials,
        'top_suppliers': top_suppliers,
    }
    return render(request, 'materials/home.html', context)

def material_catalog(request):
    """Browse material catalog"""
    materials = Material.objects.filter(is_available=True)
    categories = MaterialCategory.objects.all()
    
    # Filtering
    category_id = request.GET.get('category')
    search_query = request.GET.get('search')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    if category_id:
        materials = materials.filter(category_id=category_id)
    
    if search_query:
        materials = materials.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(brand__icontains=search_query)
        )
    
    if min_price:
        materials = materials.filter(current_price__gte=min_price)
    
    if max_price:
        materials = materials.filter(current_price__lte=max_price)
    
    context = {
        'title': 'Material Catalog',
        'materials': materials,
        'categories': categories,
        'selected_category': int(category_id) if category_id else None,
        'search_query': search_query,
        'min_price': min_price,
        'max_price': max_price,
    }
    return render(request, 'materials/catalog.html', context)

def material_detail(request, material_id):
    """Material detail page"""
    material = get_object_or_404(Material, id=material_id)
    suppliers = SupplierMaterial.objects.filter(material=material, availability=True)
    price_history = PriceHistory.objects.filter(material=material)[:10]
    
    context = {
        'title': material.name,
        'material': material,
        'suppliers': suppliers,
        'price_history': price_history,
    }
    return render(request, 'materials/material_detail.html', context)

def supplier_directory(request):
    """Supplier directory"""
    suppliers = Supplier.objects.filter(is_active=True)
    
    # Filtering
    search_query = request.GET.get('search')
    verified_only = request.GET.get('verified_only')
    
    if search_query:
        suppliers = suppliers.filter(
            Q(name__icontains=search_query) |
            Q(contact_person__icontains=search_query) |
            Q(address__icontains=search_query)
        )
    
    if verified_only:
        suppliers = suppliers.filter(is_verified=True)
    
    context = {
        'title': 'Supplier Directory',
        'suppliers': suppliers,
        'search_query': search_query,
        'verified_only': verified_only,
    }
    return render(request, 'materials/supplier_directory.html', context)

def cost_calculator(request):
    """Material cost calculator"""
    categories = MaterialCategory.objects.all()
    calculators = MaterialCalculator.objects.filter(is_active=True)
    
    context = {
        'title': 'Cost Calculator',
        'categories': categories,
        'calculators': calculators,
    }
    return render(request, 'materials/cost_calculator.html', context)

@login_required
def my_estimates(request):
    """User's project estimates"""
    estimates = ProjectEstimate.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'title': 'My Estimates',
        'estimates': estimates,
    }
    return render(request, 'materials/my_estimates.html', context)

@login_required
def create_estimate(request):
    """Create new project estimate"""
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        project_type = request.POST.get('project_type')
        total_area = request.POST.get('total_area')
        
        estimate = ProjectEstimate.objects.create(
            user=request.user,
            name=name,
            description=description,
            project_type=project_type,
            total_area=float(total_area)
        )
        
        messages.success(request, f'Estimate "{name}" created successfully!')
        return redirect('materials:estimate_detail', estimate_id=estimate.id)
    
    context = {
        'title': 'Create New Estimate',
        'project_types': ProjectEstimate._meta.get_field('project_type').choices,
    }
    return render(request, 'materials/create_estimate.html', context)

@login_required
def estimate_detail(request, estimate_id):
    """Project estimate detail"""
    estimate = get_object_or_404(ProjectEstimate, id=estimate_id, user=request.user)
    items = estimate.items.all()
    
    # Calculate totals
    total_material_cost = sum(item.total_price for item in items)
    estimate.material_cost = total_material_cost
    estimate.labor_cost = total_material_cost * 0.6  # 60% of material cost
    estimate.overhead_cost = (estimate.material_cost + estimate.labor_cost) * 0.15  # 15% overhead
    estimate.total_cost = estimate.material_cost + estimate.labor_cost + estimate.overhead_cost
    estimate.save()
    
    context = {
        'title': f'Estimate: {estimate.name}',
        'estimate': estimate,
        'items': items,
    }
    return render(request, 'materials/estimate_detail.html', context)

@api_view(['POST'])
def calculate_materials(request):
    """API endpoint to calculate material requirements"""
    calculator_id = request.data.get('calculator_id')
    parameters = request.data.get('parameters', {})
    
    if not calculator_id:
        return Response({'error': 'calculator_id is required'}, status=400)
    
    try:
        calculator = MaterialCalculator.objects.get(id=calculator_id, is_active=True)
    except MaterialCalculator.DoesNotExist:
        return Response({'error': 'Calculator not found'}, status=404)
    
    try:
        # Simple calculation examples (in production, use safe evaluation)
        results = {}
        
        if calculator.name == "Concrete Foundation":
            length = float(parameters.get('length', 0))
            width = float(parameters.get('width', 0))
            thickness = float(parameters.get('thickness', 0.5))
            
            concrete_cuyd = (length * width * thickness) / 27
            rebar_tons = concrete_cuyd * 0.1
            
            results = {
                'concrete': {'quantity': round(concrete_cuyd, 2), 'unit': 'cubic yards'},
                'rebar': {'quantity': round(rebar_tons, 2), 'unit': 'tons'},
            }
        
        elif calculator.name == "Framing Lumber":
            area = float(parameters.get('area', 0))
            floors = int(parameters.get('floors', 1))
            
            lumber_bdft = area * floors * 6
            nails_lbs = lumber_bdft * 0.01
            
            results = {
                'lumber': {'quantity': round(lumber_bdft, 2), 'unit': 'board feet'},
                'nails': {'quantity': round(nails_lbs, 2), 'unit': 'pounds'},
            }
        
        # Update usage count
        calculator.usage_count += 1
        calculator.save()
        
        return Response({
            'success': True,
            'calculator': calculator.name,
            'results': results,
            'parameters_used': parameters
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=500)

@api_view(['POST'])
def add_estimate_item(request):
    """Add item to project estimate"""
    estimate_id = request.data.get('estimate_id')
    material_id = request.data.get('material_id')
    quantity = request.data.get('quantity')
    
    if not all([estimate_id, material_id, quantity]):
        return Response({'error': 'estimate_id, material_id, and quantity are required'}, status=400)
    
    try:
        estimate = ProjectEstimate.objects.get(id=estimate_id, user=request.user)
        material = Material.objects.get(id=material_id)
        
        # Check if item already exists
        existing_item = EstimateItem.objects.filter(estimate=estimate, material=material).first()
        
        if existing_item:
            existing_item.quantity += float(quantity)
            existing_item.save()
            item = existing_item
        else:
            item = EstimateItem.objects.create(
                estimate=estimate,
                material=material,
                quantity=float(quantity),
                unit_price=material.current_price
            )
        
        return Response({
            'success': True,
            'item_id': item.id,
            'material_name': material.name,
            'quantity': item.quantity,
            'unit_price': float(item.unit_price),
            'total_price': float(item.total_price)
        })
        
    except ProjectEstimate.DoesNotExist:
        return Response({'error': 'Estimate not found'}, status=404)
    except Material.DoesNotExist:
        return Response({'error': 'Material not found'}, status=404)

@api_view(['GET'])
def price_comparison(request):
    """Compare prices across suppliers for a material"""
    material_id = request.GET.get('material_id')
    
    if not material_id:
        return Response({'error': 'material_id is required'}, status=400)
    
    try:
        material = Material.objects.get(id=material_id)
        supplier_materials = SupplierMaterial.objects.filter(
            material=material,
            availability=True
        ).select_related('supplier')
        
        price_data = []
        for sm in supplier_materials:
            price_data.append({
                'supplier_name': sm.supplier.name,
                'supplier_id': sm.supplier.id,
                'price': float(sm.supplier_price),
                'lead_time': sm.lead_time_days,
                'minimum_order': sm.minimum_order,
                'supplier_rating': sm.supplier.rating
            })
        
        # Sort by price
        price_data.sort(key=lambda x: x['price'])
        
        return Response({
            'material_name': material.name,
            'material_id': material.id,
            'base_price': float(material.base_price),
            'current_price': float(material.current_price),
            'supplier_prices': price_data,
            'lowest_price': price_data[0]['price'] if price_data else None,
            'highest_price': price_data[-1]['price'] if price_data else None
        })
        
    except Material.DoesNotExist:
        return Response({'error': 'Material not found'}, status=404)

@api_view(['GET'])
def material_search(request):
    """Search materials API"""
    query = request.GET.get('q', '')
    category_id = request.GET.get('category')
    limit = int(request.GET.get('limit', 20))
    
    materials = Material.objects.filter(is_available=True)
    
    if query:
        materials = materials.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(brand__icontains=query)
        )
    
    if category_id:
        materials = materials.filter(category_id=category_id)
    
    materials = materials[:limit]
    
    results = []
    for material in materials:
        results.append({
            'id': material.id,
            'name': material.name,
            'category': material.category.name,
            'unit': material.unit,
            'current_price': float(material.current_price),
            'brand': material.brand,
            'is_available': material.is_available
        })
    
    return Response({
        'query': query,
        'results': results,
        'total_found': len(results)
    })
