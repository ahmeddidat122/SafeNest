from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import (
    ArchitecturalProject, FloorPlan, Room, MaterialEstimate,
    AIGenerationHistory, ProjectShare, ProjectComment
)
import json
import uuid
import time
import random

def architecture_home(request):
    """Architecture design home page"""
    featured_projects = ArchitecturalProject.objects.filter(
        projectshare__is_public=True
    ).order_by('-created_at')[:6]
    
    context = {
        'title': 'AI Architecture Design',
        'featured_projects': featured_projects,
    }
    return render(request, 'architecture/home.html', context)

@login_required
def ai_generator(request):
    """AI model generator interface"""
    user_projects = ArchitecturalProject.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    context = {
        'title': 'AI Architecture Generator',
        'user_projects': user_projects,
        'project_types': ArchitecturalProject.PROJECT_TYPES,
        'style_types': ArchitecturalProject.STYLE_TYPES,
    }
    return render(request, 'architecture/ai_generator.html', context)

@login_required
def project_gallery(request):
    """User's project gallery"""
    user_projects = ArchitecturalProject.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'title': 'My Projects',
        'user_projects': user_projects,
    }
    return render(request, 'architecture/project_gallery.html', context)

def project_detail(request, project_id):
    """Project detail view"""
    project = get_object_or_404(ArchitecturalProject, id=project_id)
    
    # Check if user can view this project
    if project.user != request.user:
        try:
            share_settings = ProjectShare.objects.get(project=project)
            if not share_settings.is_public:
                messages.error(request, 'This project is private.')
                return redirect('architecture:home')
            # Increment view count
            share_settings.view_count += 1
            share_settings.save()
        except ProjectShare.DoesNotExist:
            messages.error(request, 'This project is not available.')
            return redirect('architecture:home')
    
    floor_plans = project.floor_plans.all()
    material_estimate = MaterialEstimate.objects.filter(project=project).first()
    comments = project.comments.filter(is_approved=True) if hasattr(project, 'comments') else []
    
    context = {
        'title': project.name,
        'project': project,
        'floor_plans': floor_plans,
        'material_estimate': material_estimate,
        'comments': comments,
        'can_edit': project.user == request.user,
    }
    return render(request, 'architecture/project_detail.html', context)

@login_required
def create_project(request):
    """Create new architectural project"""
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        project_type = request.POST.get('project_type')
        architectural_style = request.POST.get('architectural_style')
        ai_prompt = request.POST.get('ai_prompt')
        
        # Optional specifications
        total_area = request.POST.get('total_area')
        bedrooms = request.POST.get('bedrooms')
        bathrooms = request.POST.get('bathrooms')
        floors = request.POST.get('floors', 1)
        
        project = ArchitecturalProject.objects.create(
            user=request.user,
            name=name,
            description=description,
            project_type=project_type,
            architectural_style=architectural_style,
            ai_prompt=ai_prompt,
            total_area=float(total_area) if total_area else None,
            bedrooms=int(bedrooms) if bedrooms else None,
            bathrooms=int(bathrooms) if bathrooms else None,
            floors=int(floors),
        )
        
        messages.success(request, f'Project "{name}" created successfully!')
        return redirect('architecture:generate_model', project_id=project.id)
    
    context = {
        'title': 'Create New Project',
        'project_types': ArchitecturalProject.PROJECT_TYPES,
        'style_types': ArchitecturalProject.STYLE_TYPES,
    }
    return render(request, 'architecture/create_project.html', context)

@login_required
def generate_model(request, project_id):
    """Generate AI model for project"""
    project = get_object_or_404(ArchitecturalProject, id=project_id, user=request.user)
    
    if request.method == 'POST':
        # Start AI generation process (simulated)
        project.generation_status = 'generating'
        project.generation_progress = 0
        project.save()
        
        # In a real implementation, this would trigger an AI model generation
        # For now, we'll simulate the process
        return JsonResponse({
            'success': True,
            'message': 'AI generation started',
            'project_id': project.id
        })
    
    context = {
        'title': f'Generate Model - {project.name}',
        'project': project,
    }
    return render(request, 'architecture/generate_model.html', context)

@api_view(['POST'])
def generate_architecture_ai(request):
    """API endpoint to generate architecture using AI"""
    prompt = request.data.get('prompt')
    project_type = request.data.get('project_type', 'residential')
    style = request.data.get('style', 'modern')
    specifications = request.data.get('specifications', {})
    
    if not prompt:
        return Response({'error': 'Prompt is required'}, status=400)
    
    # Simulate AI generation process
    generation_start = time.time()
    
    # Create generation history record
    history = AIGenerationHistory.objects.create(
        user=request.user,
        prompt=prompt,
        generation_type='3d_model',
        model_version='v1.0'
    )
    
    try:
        # Simulate AI processing time
        time.sleep(2)
        
        # Generate mock results
        mock_results = {
            '3d_model_url': f'/media/models/generated_{uuid.uuid4().hex[:8]}.obj',
            'floor_plan_url': f'/media/floorplans/plan_{uuid.uuid4().hex[:8]}.png',
            'exterior_views': [
                f'/media/renders/exterior_{uuid.uuid4().hex[:8]}.jpg',
                f'/media/renders/exterior_{uuid.uuid4().hex[:8]}.jpg'
            ],
            'interior_views': [
                f'/media/renders/interior_{uuid.uuid4().hex[:8]}.jpg',
                f'/media/renders/interior_{uuid.uuid4().hex[:8]}.jpg'
            ],
            'specifications': {
                'total_area': random.randint(1200, 3500),
                'bedrooms': random.randint(2, 5),
                'bathrooms': random.randint(1, 4),
                'floors': random.randint(1, 3)
            }
        }
        
        generation_time = time.time() - generation_start
        
        # Update history record
        history.success = True
        history.result_data = mock_results
        history.generation_time_seconds = generation_time
        history.save()
        
        return Response({
            'success': True,
            'generation_id': history.id,
            'results': mock_results,
            'generation_time': generation_time,
            'message': 'AI model generated successfully'
        })
        
    except Exception as e:
        # Update history record with error
        history.success = False
        history.error_message = str(e)
        history.generation_time_seconds = time.time() - generation_start
        history.save()
        
        return Response({
            'success': False,
            'error': str(e),
            'generation_id': history.id
        }, status=500)

@api_view(['POST'])
def estimate_materials(request):
    """API endpoint to estimate materials and costs"""
    project_id = request.data.get('project_id')
    
    if not project_id:
        return Response({'error': 'project_id is required'}, status=400)
    
    try:
        project = ArchitecturalProject.objects.get(id=project_id, user=request.user)
    except ArchitecturalProject.DoesNotExist:
        return Response({'error': 'Project not found'}, status=404)
    
    # Calculate material estimates based on project specifications
    total_area = project.total_area or 2000  # Default area
    floors = project.floors or 1
    
    # Basic material calculations (simplified)
    concrete_needed = (total_area * 0.5) / 27  # Cubic yards
    steel_needed = total_area * 0.02  # Tons
    lumber_needed = total_area * 6  # Board feet
    bricks_needed = int(total_area * 7)  # Count
    
    # Cost estimates (simplified)
    material_cost = (
        concrete_needed * 100 +  # $100 per cubic yard
        steel_needed * 800 +     # $800 per ton
        lumber_needed * 2 +      # $2 per board foot
        bricks_needed * 0.5      # $0.50 per brick
    )
    
    labor_cost = material_cost * 1.5  # Labor is typically 1.5x material cost
    total_cost = material_cost + labor_cost
    
    # Create or update material estimate
    estimate, created = MaterialEstimate.objects.update_or_create(
        project=project,
        defaults={
            'concrete_cubic_yards': concrete_needed,
            'steel_tons': steel_needed,
            'lumber_board_feet': lumber_needed,
            'bricks_count': bricks_needed,
            'material_cost': material_cost,
            'labor_cost': labor_cost,
            'total_estimated_cost': total_cost,
            'detailed_breakdown': {
                'concrete': {'quantity': concrete_needed, 'unit_cost': 100, 'total': concrete_needed * 100},
                'steel': {'quantity': steel_needed, 'unit_cost': 800, 'total': steel_needed * 800},
                'lumber': {'quantity': lumber_needed, 'unit_cost': 2, 'total': lumber_needed * 2},
                'bricks': {'quantity': bricks_needed, 'unit_cost': 0.5, 'total': bricks_needed * 0.5},
            }
        }
    )
    
    return Response({
        'success': True,
        'estimate_id': estimate.id,
        'materials': {
            'concrete_cubic_yards': concrete_needed,
            'steel_tons': steel_needed,
            'lumber_board_feet': lumber_needed,
            'bricks_count': bricks_needed,
        },
        'costs': {
            'material_cost': float(material_cost),
            'labor_cost': float(labor_cost),
            'total_cost': float(total_cost),
        },
        'detailed_breakdown': estimate.detailed_breakdown
    })

@api_view(['GET'])
def generation_progress(request, project_id):
    """Get generation progress for a project"""
    try:
        project = ArchitecturalProject.objects.get(id=project_id, user=request.user)
        
        # Simulate progress updates
        if project.generation_status == 'generating':
            # Randomly update progress
            if project.generation_progress < 100:
                project.generation_progress = min(100, project.generation_progress + random.randint(10, 30))
                if project.generation_progress >= 100:
                    project.generation_status = 'completed'
                    project.is_generated = True
                project.save()
        
        return Response({
            'project_id': project.id,
            'status': project.generation_status,
            'progress': project.generation_progress,
            'is_completed': project.is_generated
        })
        
    except ArchitecturalProject.DoesNotExist:
        return Response({'error': 'Project not found'}, status=404)

@login_required
def share_project(request, project_id):
    """Share project settings"""
    project = get_object_or_404(ArchitecturalProject, id=project_id, user=request.user)
    
    if request.method == 'POST':
        is_public = request.POST.get('is_public') == 'on'
        allow_comments = request.POST.get('allow_comments') == 'on'
        allow_downloads = request.POST.get('allow_downloads') == 'on'
        
        share_settings, created = ProjectShare.objects.update_or_create(
            project=project,
            defaults={
                'is_public': is_public,
                'allow_comments': allow_comments,
                'allow_downloads': allow_downloads,
                'share_token': uuid.uuid4().hex if is_public else ''
            }
        )
        
        messages.success(request, 'Share settings updated successfully!')
        return redirect('architecture:project_detail', project_id=project.id)
    
    try:
        share_settings = ProjectShare.objects.get(project=project)
    except ProjectShare.DoesNotExist:
        share_settings = None
    
    context = {
        'title': f'Share {project.name}',
        'project': project,
        'share_settings': share_settings,
    }
    return render(request, 'architecture/share_project.html', context)
