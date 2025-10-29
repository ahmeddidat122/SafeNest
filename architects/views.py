from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Avg
from django.core.paginator import Paginator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import (
    ArchitectProfile, ArchitectPortfolio, ArchitectReview,
    ArchitectInquiry, ArchitectCertification, ArchitectService
)
from datetime import datetime

def architect_directory(request):
    """Main architect directory page"""
    architects = ArchitectProfile.objects.filter(is_available=True)
    
    # Filtering
    specialization = request.GET.get('specialization')
    location = request.GET.get('location')
    min_rating = request.GET.get('min_rating')
    search_query = request.GET.get('search')
    
    if specialization:
        architects = architects.filter(specializations__contains=[specialization])
    
    if location:
        architects = architects.filter(
            Q(city__icontains=location) |
            Q(state__icontains=location)
        )
    
    if min_rating:
        architects = architects.filter(average_rating__gte=float(min_rating))
    
    if search_query:
        architects = architects.filter(
            Q(firm_name__icontains=search_query) |
            Q(contact_person__icontains=search_query) |
            Q(bio__icontains=search_query)
        )
    
    # Sorting
    sort_by = request.GET.get('sort', 'rating')
    if sort_by == 'rating':
        architects = architects.order_by('-average_rating', '-total_reviews')
    elif sort_by == 'experience':
        architects = architects.order_by('-years_experience')
    elif sort_by == 'projects':
        architects = architects.order_by('-total_projects')
    elif sort_by == 'name':
        architects = architects.order_by('firm_name')
    
    # Pagination
    paginator = Paginator(architects, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Featured architects
    featured_architects = ArchitectProfile.objects.filter(
        is_featured=True, is_available=True
    )[:3]
    
    context = {
        'title': 'Find Local Architects',
        'page_obj': page_obj,
        'featured_architects': featured_architects,
        'specializations': ArchitectProfile.SPECIALIZATIONS,
        'selected_specialization': specialization,
        'selected_location': location,
        'selected_rating': min_rating,
        'search_query': search_query,
        'sort_by': sort_by,
        'total_architects': paginator.count,
    }
    return render(request, 'architects/directory.html', context)

def architect_profile(request, architect_id):
    """Individual architect profile page"""
    architect = get_object_or_404(ArchitectProfile, id=architect_id, is_available=True)
    portfolio = architect.portfolio.filter(is_featured=True)[:6]
    reviews = architect.reviews.filter(is_approved=True)[:5]
    services = architect.services.filter(is_available=True)
    certifications = architect.certifications.filter(is_active=True)
    
    context = {
        'title': architect.firm_name,
        'architect': architect,
        'portfolio': portfolio,
        'reviews': reviews,
        'services': services,
        'certifications': certifications,
        'avg_ratings': {
            'design_quality': reviews.aggregate(avg=Avg('design_quality'))['avg'] or 0,
            'communication': reviews.aggregate(avg=Avg('communication'))['avg'] or 0,
            'timeliness': reviews.aggregate(avg=Avg('timeliness'))['avg'] or 0,
            'budget_adherence': reviews.aggregate(avg=Avg('budget_adherence'))['avg'] or 0,
        }
    }
    return render(request, 'architects/profile.html', context)

def architect_portfolio_detail(request, architect_id, portfolio_id):
    """Portfolio project detail page"""
    architect = get_object_or_404(ArchitectProfile, id=architect_id)
    portfolio_item = get_object_or_404(ArchitectPortfolio, id=portfolio_id, architect=architect)
    
    # Related portfolio items
    related_portfolio = architect.portfolio.exclude(id=portfolio_id)[:4]
    
    context = {
        'title': portfolio_item.title,
        'architect': architect,
        'portfolio_item': portfolio_item,
        'related_portfolio': related_portfolio,
    }
    return render(request, 'architects/portfolio_detail.html', context)

def send_inquiry(request, architect_id):
    """Send inquiry to architect"""
    architect = get_object_or_404(ArchitectProfile, id=architect_id, is_available=True)
    
    if request.method == 'POST':
        client_name = request.POST.get('client_name')
        client_email = request.POST.get('client_email')
        client_phone = request.POST.get('client_phone')
        inquiry_type = request.POST.get('inquiry_type')
        project_title = request.POST.get('project_title')
        project_description = request.POST.get('project_description')
        project_location = request.POST.get('project_location')
        estimated_budget = request.POST.get('estimated_budget')
        timeline = request.POST.get('timeline')
        
        inquiry = ArchitectInquiry.objects.create(
            architect=architect,
            client_name=client_name,
            client_email=client_email,
            client_phone=client_phone,
            inquiry_type=inquiry_type,
            project_title=project_title,
            project_description=project_description,
            project_location=project_location,
            estimated_budget=estimated_budget,
            timeline=timeline
        )
        
        messages.success(request, f'Your inquiry has been sent to {architect.firm_name}!')
        return redirect('architects:profile', architect_id=architect.id)
    
    context = {
        'title': f'Contact {architect.firm_name}',
        'architect': architect,
        'inquiry_types': ArchitectInquiry.INQUIRY_TYPES,
    }
    return render(request, 'architects/send_inquiry.html', context)

def submit_review(request, architect_id):
    """Submit review for architect"""
    architect = get_object_or_404(ArchitectProfile, id=architect_id)
    
    if request.method == 'POST':
        client_name = request.POST.get('client_name')
        client_email = request.POST.get('client_email')
        rating = int(request.POST.get('rating'))
        title = request.POST.get('title')
        review_text = request.POST.get('review_text')
        project_type = request.POST.get('project_type')
        project_duration = request.POST.get('project_duration')
        project_budget = request.POST.get('project_budget')
        
        # Individual ratings
        design_quality = request.POST.get('design_quality')
        communication = request.POST.get('communication')
        timeliness = request.POST.get('timeliness')
        budget_adherence = request.POST.get('budget_adherence')
        
        review = ArchitectReview.objects.create(
            architect=architect,
            client_name=client_name,
            client_email=client_email,
            rating=rating,
            title=title,
            review_text=review_text,
            project_type=project_type,
            project_duration=project_duration,
            project_budget=project_budget,
            design_quality=int(design_quality) if design_quality else None,
            communication=int(communication) if communication else None,
            timeliness=int(timeliness) if timeliness else None,
            budget_adherence=int(budget_adherence) if budget_adherence else None,
        )
        
        # Update architect's average rating
        reviews = architect.reviews.filter(is_approved=True)
        architect.average_rating = reviews.aggregate(avg=Avg('rating'))['avg'] or 0
        architect.total_reviews = reviews.count()
        architect.save()
        
        messages.success(request, 'Thank you for your review!')
        return redirect('architects:profile', architect_id=architect.id)
    
    context = {
        'title': f'Review {architect.firm_name}',
        'architect': architect,
        'specializations': ArchitectProfile.SPECIALIZATIONS,
    }
    return render(request, 'architects/submit_review.html', context)

@login_required
def architect_dashboard(request):
    """Dashboard for architect users"""
    try:
        architect = ArchitectProfile.objects.get(user=request.user)
    except ArchitectProfile.DoesNotExist:
        messages.info(request, 'Please complete your architect profile.')
        return redirect('architects:create_profile')
    
    recent_inquiries = architect.inquiries.all()[:5]
    recent_reviews = architect.reviews.filter(is_approved=True)[:5]
    portfolio_count = architect.portfolio.count()
    
    context = {
        'title': 'Architect Dashboard',
        'architect': architect,
        'recent_inquiries': recent_inquiries,
        'recent_reviews': recent_reviews,
        'portfolio_count': portfolio_count,
        'total_inquiries': architect.inquiries.count(),
        'pending_inquiries': architect.inquiries.filter(status='pending').count(),
    }
    return render(request, 'architects/dashboard.html', context)

@api_view(['GET'])
def search_architects(request):
    """API endpoint to search architects"""
    query = request.GET.get('q', '')
    specialization = request.GET.get('specialization')
    location = request.GET.get('location')
    limit = int(request.GET.get('limit', 10))
    
    architects = ArchitectProfile.objects.filter(is_available=True)
    
    if query:
        architects = architects.filter(
            Q(firm_name__icontains=query) |
            Q(contact_person__icontains=query) |
            Q(bio__icontains=query)
        )
    
    if specialization:
        architects = architects.filter(specializations__contains=[specialization])
    
    if location:
        architects = architects.filter(
            Q(city__icontains=location) |
            Q(state__icontains=location)
        )
    
    architects = architects.order_by('-average_rating')[:limit]
    
    results = []
    for architect in architects:
        results.append({
            'id': architect.id,
            'firm_name': architect.firm_name,
            'contact_person': architect.contact_person,
            'city': architect.city,
            'state': architect.state,
            'specializations': architect.specializations,
            'average_rating': architect.average_rating,
            'total_reviews': architect.total_reviews,
            'years_experience': architect.years_experience,
            'profile_image': architect.profile_image,
            'is_verified': architect.is_verified
        })
    
    return Response({
        'query': query,
        'results': results,
        'total_found': len(results)
    })

@api_view(['POST'])
def quick_inquiry(request):
    """Quick inquiry API endpoint"""
    architect_id = request.data.get('architect_id')
    client_name = request.data.get('client_name')
    client_email = request.data.get('client_email')
    message = request.data.get('message')
    
    if not all([architect_id, client_name, client_email, message]):
        return Response({'error': 'All fields are required'}, status=400)
    
    try:
        architect = ArchitectProfile.objects.get(id=architect_id, is_available=True)
        
        inquiry = ArchitectInquiry.objects.create(
            architect=architect,
            client_name=client_name,
            client_email=client_email,
            inquiry_type='consultation',
            project_title='Quick Inquiry',
            project_description=message
        )
        
        return Response({
            'success': True,
            'inquiry_id': inquiry.id,
            'message': f'Your inquiry has been sent to {architect.firm_name}'
        })
        
    except ArchitectProfile.DoesNotExist:
        return Response({'error': 'Architect not found'}, status=404)

@api_view(['GET'])
def architect_stats(request):
    """Get architect directory statistics"""
    total_architects = ArchitectProfile.objects.filter(is_available=True).count()
    verified_architects = ArchitectProfile.objects.filter(is_available=True, is_verified=True).count()
    total_reviews = ArchitectReview.objects.filter(is_approved=True).count()
    avg_rating = ArchitectReview.objects.filter(is_approved=True).aggregate(avg=Avg('rating'))['avg'] or 0
    
    specialization_counts = {}
    for spec_code, spec_name in ArchitectProfile.SPECIALIZATIONS:
        count = ArchitectProfile.objects.filter(
            is_available=True,
            specializations__contains=[spec_code]
        ).count()
        specialization_counts[spec_name] = count
    
    return Response({
        'total_architects': total_architects,
        'verified_architects': verified_architects,
        'total_reviews': total_reviews,
        'average_rating': round(avg_rating, 2),
        'specialization_counts': specialization_counts
    })
