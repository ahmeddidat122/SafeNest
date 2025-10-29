from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Appliance, UserEnergyProfile, EnergyReading, EnergyTip
import json

def energy_calculator(request):
    """Energy consumption calculator page"""
    appliances = Appliance.objects.all()
    energy_tips = EnergyTip.objects.filter(is_active=True)[:5]
    
    context = {
        'title': 'Energy Consumption Calculator',
        'appliances': appliances,
        'energy_tips': energy_tips,
    }
    return render(request, 'energy/calculator.html', context)

@login_required
def energy_dashboard(request):
    """User's energy dashboard"""
    try:
        profile = UserEnergyProfile.objects.get(user=request.user)
    except UserEnergyProfile.DoesNotExist:
        profile = UserEnergyProfile.objects.create(user=request.user)
    
    recent_readings = EnergyReading.objects.filter(user=request.user)[:10]
    
    context = {
        'title': 'Energy Dashboard',
        'profile': profile,
        'recent_readings': recent_readings,
        'total_appliances': profile.appliances.count(),
        'monthly_consumption': profile.total_monthly_consumption,
        'estimated_bill': profile.estimated_monthly_bill,
    }
    return render(request, 'energy/dashboard.html', context)

@login_required
def add_appliance(request):
    """Add appliance to user's profile"""
    if request.method == 'POST':
        appliance_id = request.POST.get('appliance_id')
        hours_per_day = float(request.POST.get('hours_per_day', 8))
        
        try:
            appliance = Appliance.objects.get(id=appliance_id)
            profile, created = UserEnergyProfile.objects.get_or_create(user=request.user)
            
            # Create a copy of the appliance with user-specific usage
            user_appliance = Appliance.objects.create(
                name=f"{request.user.username}'s {appliance.name}",
                appliance_type=appliance.appliance_type,
                power_rating=appliance.power_rating,
                hours_per_day=hours_per_day,
                energy_star_rating=appliance.energy_star_rating
            )
            
            profile.appliances.add(user_appliance)
            messages.success(request, f'{appliance.name} added to your energy profile!')
            
        except Appliance.DoesNotExist:
            messages.error(request, 'Appliance not found.')
    
    return redirect('energy:dashboard')

@login_required
def remove_appliance(request, appliance_id):
    """Remove appliance from user's profile"""
    try:
        profile = UserEnergyProfile.objects.get(user=request.user)
        appliance = get_object_or_404(Appliance, id=appliance_id)
        profile.appliances.remove(appliance)
        appliance.delete()  # Delete the user-specific copy
        messages.success(request, 'Appliance removed from your profile.')
    except UserEnergyProfile.DoesNotExist:
        messages.error(request, 'Energy profile not found.')
    
    return redirect('energy:dashboard')

def energy_tips(request):
    """Energy saving tips page"""
    tips = EnergyTip.objects.filter(is_active=True)
    
    # Filter by category if specified
    category = request.GET.get('category')
    if category:
        tips = tips.filter(category=category)
    
    context = {
        'title': 'Energy Saving Tips',
        'tips': tips,
        'categories': EnergyTip._meta.get_field('category').choices,
        'selected_category': category,
    }
    return render(request, 'energy/tips.html', context)

@api_view(['POST'])
def calculate_consumption(request):
    """API endpoint to calculate energy consumption"""
    appliances_data = request.data.get('appliances', [])
    electricity_rate = float(request.data.get('electricity_rate', 0.12))
    
    total_consumption = 0
    appliance_details = []
    
    for appliance_data in appliances_data:
        power_rating = float(appliance_data.get('power_rating', 0))
        hours_per_day = float(appliance_data.get('hours_per_day', 8))
        
        daily_kwh = (power_rating * hours_per_day) / 1000
        monthly_kwh = daily_kwh * 30
        monthly_cost = monthly_kwh * electricity_rate
        
        total_consumption += monthly_kwh
        
        appliance_details.append({
            'name': appliance_data.get('name', 'Unknown'),
            'daily_kwh': round(daily_kwh, 2),
            'monthly_kwh': round(monthly_kwh, 2),
            'monthly_cost': round(monthly_cost, 2)
        })
    
    total_monthly_cost = total_consumption * electricity_rate
    
    return Response({
        'total_monthly_consumption': round(total_consumption, 2),
        'total_monthly_cost': round(total_monthly_cost, 2),
        'appliance_details': appliance_details,
        'electricity_rate': electricity_rate
    })

@api_view(['POST'])
def log_energy_reading(request):
    """API endpoint for IoT devices to log energy readings"""
    device_id = request.data.get('device_id')
    power_consumption = request.data.get('power_consumption')
    voltage = request.data.get('voltage')
    current = request.data.get('current')
    
    if not device_id or power_consumption is None:
        return Response({'error': 'device_id and power_consumption are required'}, status=400)
    
    # For now, we'll use a default user. In production, this would be authenticated
    from django.contrib.auth.models import User
    user = User.objects.first()  # This should be properly authenticated
    
    reading = EnergyReading.objects.create(
        user=user,
        device_id=device_id,
        power_consumption=float(power_consumption),
        voltage=float(voltage) if voltage else None,
        current=float(current) if current else None
    )
    
    return Response({
        'status': 'success',
        'reading_id': reading.id,
        'timestamp': reading.timestamp
    })

@api_view(['GET'])
def energy_stats(request):
    """API endpoint to get energy statistics"""
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=401)
    
    try:
        profile = UserEnergyProfile.objects.get(user=request.user)
        recent_readings = EnergyReading.objects.filter(user=request.user)[:24]  # Last 24 readings
        
        return Response({
            'total_appliances': profile.appliances.count(),
            'monthly_consumption': profile.total_monthly_consumption,
            'estimated_monthly_bill': profile.estimated_monthly_bill,
            'electricity_rate': profile.electricity_rate,
            'recent_readings': [
                {
                    'device_id': reading.device_id,
                    'power_consumption': reading.power_consumption,
                    'timestamp': reading.timestamp
                } for reading in recent_readings
            ]
        })
    except UserEnergyProfile.DoesNotExist:
        return Response({'error': 'Energy profile not found'}, status=404)
