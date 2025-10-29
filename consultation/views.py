from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Avg
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import (
    ConsultationSession, ChatMessage, Consultant, ConsultationRequest,
    ConsultationFeedback, ConsultationResource
)
from datetime import datetime, timedelta
import json

def consultation_home(request):
    """Consultation service home page"""
    available_consultants = Consultant.objects.filter(is_available=True)[:6]
    recent_sessions = ConsultationSession.objects.filter(status='completed')[:5]
    
    context = {
        'title': 'Live Expert Consultation',
        'available_consultants': available_consultants,
        'recent_sessions': recent_sessions,
        'consultation_types': ConsultationSession.SESSION_TYPES,
    }
    return render(request, 'consultation/home.html', context)

def find_consultants(request):
    """Find and browse consultants"""
    consultants = Consultant.objects.filter(is_available=True)
    
    # Filtering
    expertise = request.GET.get('expertise')
    min_rating = request.GET.get('min_rating')
    max_rate = request.GET.get('max_rate')
    search_query = request.GET.get('search')
    
    if expertise:
        consultants = consultants.filter(expertise_areas__contains=[expertise])
    
    if min_rating:
        consultants = consultants.filter(average_rating__gte=float(min_rating))
    
    if max_rate:
        consultants = consultants.filter(hourly_rate__lte=float(max_rate))
    
    if search_query:
        consultants = consultants.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(title__icontains=search_query) |
            Q(bio__icontains=search_query)
        )
    
    # Sorting
    sort_by = request.GET.get('sort', 'rating')
    if sort_by == 'rating':
        consultants = consultants.order_by('-average_rating')
    elif sort_by == 'experience':
        consultants = consultants.order_by('-years_experience')
    elif sort_by == 'rate_low':
        consultants = consultants.order_by('hourly_rate')
    elif sort_by == 'rate_high':
        consultants = consultants.order_by('-hourly_rate')
    
    context = {
        'title': 'Find Consultants',
        'consultants': consultants,
        'expertise_areas': Consultant.EXPERTISE_AREAS,
        'selected_expertise': expertise,
        'selected_rating': min_rating,
        'selected_max_rate': max_rate,
        'search_query': search_query,
        'sort_by': sort_by,
    }
    return render(request, 'consultation/find_consultants.html', context)

def consultant_profile(request, consultant_id):
    """Individual consultant profile"""
    consultant = get_object_or_404(Consultant, id=consultant_id, is_available=True)
    recent_sessions = ConsultationSession.objects.filter(
        consultant=consultant.user, status='completed'
    )[:5]
    
    context = {
        'title': f'{consultant.user.get_full_name()} - {consultant.title}',
        'consultant': consultant,
        'recent_sessions': recent_sessions,
    }
    return render(request, 'consultation/consultant_profile.html', context)

@login_required
def request_consultation(request, consultant_id=None):
    """Request a consultation"""
    consultant = None
    if consultant_id:
        consultant = get_object_or_404(Consultant, id=consultant_id, is_available=True)
    
    if request.method == 'POST':
        consultation_type = request.POST.get('consultation_type')
        title = request.POST.get('title')
        description = request.POST.get('description')
        urgency = request.POST.get('urgency')
        duration_needed = request.POST.get('duration_needed', 30)
        budget_range = request.POST.get('budget_range')
        
        consultation_request = ConsultationRequest.objects.create(
            client=request.user,
            consultant=consultant,
            consultation_type=consultation_type,
            title=title,
            description=description,
            urgency=urgency,
            duration_needed=int(duration_needed),
            budget_range=budget_range
        )
        
        messages.success(request, 'Your consultation request has been submitted!')
        return redirect('consultation:my_requests')
    
    context = {
        'title': 'Request Consultation',
        'consultant': consultant,
        'consultation_types': ConsultationSession.SESSION_TYPES,
        'urgency_levels': ConsultationRequest.URGENCY_LEVELS,
    }
    return render(request, 'consultation/request_consultation.html', context)

@login_required
def my_consultations(request):
    """User's consultation sessions"""
    sessions = ConsultationSession.objects.filter(client=request.user).order_by('-created_at')
    requests = ConsultationRequest.objects.filter(client=request.user).order_by('-created_at')
    
    context = {
        'title': 'My Consultations',
        'sessions': sessions,
        'requests': requests,
    }
    return render(request, 'consultation/my_consultations.html', context)

@login_required
def my_requests(request):
    """User's consultation requests"""
    requests = ConsultationRequest.objects.filter(client=request.user).order_by('-created_at')
    
    context = {
        'title': 'My Consultation Requests',
        'requests': requests,
    }
    return render(request, 'consultation/my_requests.html', context)

@login_required
def chat_session(request, session_id):
    """Live chat session"""
    session = get_object_or_404(ConsultationSession, id=session_id)
    
    # Check if user is authorized to access this session
    if session.client != request.user and session.consultant != request.user:
        messages.error(request, 'You are not authorized to access this session.')
        return redirect('consultation:my_consultations')
    
    messages = session.messages.all()
    
    context = {
        'title': f'Chat: {session.title}',
        'session': session,
        'messages': messages,
        'is_consultant': session.consultant == request.user,
    }
    return render(request, 'consultation/chat_session.html', context)

@login_required
def session_feedback(request, session_id):
    """Submit feedback for a session"""
    session = get_object_or_404(ConsultationSession, id=session_id, client=request.user, status='completed')
    
    if request.method == 'POST':
        overall_rating = int(request.POST.get('overall_rating'))
        consultant_knowledge = int(request.POST.get('consultant_knowledge'))
        communication_quality = int(request.POST.get('communication_quality'))
        problem_solving = int(request.POST.get('problem_solving'))
        value_for_money = int(request.POST.get('value_for_money'))
        what_went_well = request.POST.get('what_went_well')
        areas_for_improvement = request.POST.get('areas_for_improvement')
        would_recommend = request.POST.get('would_recommend') == 'on'
        additional_comments = request.POST.get('additional_comments')
        
        feedback = ConsultationFeedback.objects.create(
            session=session,
            overall_rating=overall_rating,
            consultant_knowledge=consultant_knowledge,
            communication_quality=communication_quality,
            problem_solving=problem_solving,
            value_for_money=value_for_money,
            what_went_well=what_went_well,
            areas_for_improvement=areas_for_improvement,
            would_recommend=would_recommend,
            additional_comments=additional_comments
        )
        
        # Update consultant's average rating
        if session.consultant:
            consultant = Consultant.objects.get(user=session.consultant)
            feedbacks = ConsultationFeedback.objects.filter(session__consultant=session.consultant)
            consultant.average_rating = feedbacks.aggregate(avg=Avg('overall_rating'))['avg'] or 0
            consultant.save()
        
        messages.success(request, 'Thank you for your feedback!')
        return redirect('consultation:my_consultations')
    
    context = {
        'title': f'Feedback: {session.title}',
        'session': session,
    }
    return render(request, 'consultation/session_feedback.html', context)

@api_view(['POST'])
def send_message(request):
    """Send message in chat session"""
    session_id = request.data.get('session_id')
    message_text = request.data.get('message')
    message_type = request.data.get('message_type', 'text')
    
    if not all([session_id, message_text]):
        return Response({'error': 'session_id and message are required'}, status=400)
    
    try:
        session = ConsultationSession.objects.get(id=session_id)
        
        # Check authorization
        if session.client != request.user and session.consultant != request.user:
            return Response({'error': 'Unauthorized'}, status=403)
        
        message = ChatMessage.objects.create(
            session=session,
            sender=request.user,
            message=message_text,
            message_type=message_type
        )
        
        return Response({
            'success': True,
            'message_id': message.id,
            'sender': request.user.get_full_name() or request.user.username,
            'message': message.message,
            'timestamp': message.timestamp.isoformat()
        })
        
    except ConsultationSession.DoesNotExist:
        return Response({'error': 'Session not found'}, status=404)

@api_view(['GET'])
def get_messages(request, session_id):
    """Get messages for a chat session"""
    try:
        session = ConsultationSession.objects.get(id=session_id)
        
        # Check authorization
        if session.client != request.user and session.consultant != request.user:
            return Response({'error': 'Unauthorized'}, status=403)
        
        messages = session.messages.all()
        
        message_data = []
        for message in messages:
            message_data.append({
                'id': message.id,
                'sender': message.sender.get_full_name() or message.sender.username,
                'sender_id': message.sender.id,
                'message': message.message,
                'message_type': message.message_type,
                'timestamp': message.timestamp.isoformat(),
                'is_own_message': message.sender == request.user
            })
        
        return Response({
            'session_id': session.id,
            'messages': message_data
        })
        
    except ConsultationSession.DoesNotExist:
        return Response({'error': 'Session not found'}, status=404)

@api_view(['POST'])
def start_session(request):
    """Start a consultation session"""
    request_id = request.data.get('request_id')
    
    if not request_id:
        return Response({'error': 'request_id is required'}, status=400)
    
    try:
        consultation_request = ConsultationRequest.objects.get(id=request_id)
        
        # Create session
        session = ConsultationSession.objects.create(
            client=consultation_request.client,
            consultant=consultation_request.assigned_consultant.user if consultation_request.assigned_consultant else None,
            session_type=consultation_request.consultation_type,
            title=consultation_request.title,
            description=consultation_request.description,
            duration_minutes=consultation_request.duration_needed,
            status='active',
            actual_start_time=datetime.now()
        )
        
        # Update request
        consultation_request.session = session
        consultation_request.status = 'scheduled'
        consultation_request.save()
        
        # Send system message
        ChatMessage.objects.create(
            session=session,
            sender=consultation_request.client,
            message=f"Consultation session started: {session.title}",
            message_type='system'
        )
        
        return Response({
            'success': True,
            'session_id': session.id,
            'message': 'Session started successfully'
        })
        
    except ConsultationRequest.DoesNotExist:
        return Response({'error': 'Request not found'}, status=404)

@api_view(['POST'])
def end_session(request):
    """End a consultation session"""
    session_id = request.data.get('session_id')
    
    if not session_id:
        return Response({'error': 'session_id is required'}, status=400)
    
    try:
        session = ConsultationSession.objects.get(id=session_id)
        
        # Check authorization
        if session.client != request.user and session.consultant != request.user:
            return Response({'error': 'Unauthorized'}, status=403)
        
        session.status = 'completed'
        session.actual_end_time = datetime.now()
        
        # Calculate duration and cost
        if session.actual_start_time:
            duration = session.actual_end_time - session.actual_start_time
            duration_hours = duration.total_seconds() / 3600
            session.total_cost = float(session.hourly_rate) * duration_hours
        
        session.save()
        
        # Send system message
        ChatMessage.objects.create(
            session=session,
            sender=request.user,
            message="Consultation session ended.",
            message_type='system'
        )
        
        return Response({
            'success': True,
            'session_id': session.id,
            'total_cost': float(session.total_cost),
            'message': 'Session ended successfully'
        })
        
    except ConsultationSession.DoesNotExist:
        return Response({'error': 'Session not found'}, status=404)
