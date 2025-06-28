from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q

from .models import Commission

def commission_list(request):
    search_query = request.GET.get('q', '')
    if search_query:
        # Search by title or client fields (nickname, handle, or email)
        commissions = Commission.objects.filter(
            Q(title__icontains=search_query) |
            Q(client__nickname__icontains=search_query) |
            Q(client__handle__icontains=search_query) |
            Q(client__email__icontains=search_query)
        )
    else:
        commissions = Commission.objects.all()
    return render(request, 'commissions/commission_list.html', {'commissions': commissions})

def commission_detail(request, commission_id):
    commission = get_object_or_404(Commission, pk=commission_id)
    return render(request, 'commissions/commission_detail.html', {'commission': commission})

def home(request):
    return render(request, 'commissions/home.html')
from django.contrib import messages
from django.db.models import Q
from .models import Commission


def commission_list(request):
    commissions = Commission.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        commissions = commissions.filter(
            Q(title__icontains=search_query) |
            Q(client_name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        commissions = commissions.filter(status=status_filter)
    
    context = {
        'commissions': commissions,
        'search_query': search_query,
        'status_filter': status_filter,
        'status_choices': Commission.STATUS_CHOICES,
    }
    return render(request, 'commissions/commission_list.html', context)


def commission_detail(request, pk):
    commission = get_object_or_404(Commission, pk=pk)
    return render(request, 'commissions/commission_detail.html', {'commission': commission})


def home(request):
    recent_commissions = Commission.objects.all()[:5]
    total_pending = Commission.objects.filter(status='pending').count()
    total_in_progress = Commission.objects.filter(status='in_progress').count()
    total_completed = Commission.objects.filter(status='completed').count()
    
    context = {
        'recent_commissions': recent_commissions,
        'total_pending': total_pending,
        'total_in_progress': total_in_progress,
        'total_completed': total_completed,
    }
    return render(request, 'commissions/home.html', context)
