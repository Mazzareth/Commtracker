from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q

from .models import Commission

def commission_list(request):
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    commissions = Commission.objects.all()

    if search_query:
        commissions = commissions.filter(
            Q(title__icontains=search_query) |
            Q(client__nickname__icontains=search_query) |
            Q(client__handle__icontains=search_query) |
            Q(client__email__icontains=search_query)
        )
    if status_filter:
        commissions = commissions.filter(status=status_filter)

    context = {
        'commissions': commissions,
        'search_query': search_query,
        'status_filter': status_filter,
    }
    return render(request, 'commissions/commission_list.html', context)

def commission_detail(request, pk):
    commission = get_object_or_404(Commission, pk=pk)
    return render(request, 'commissions/commission_detail.html', {'commission': commission})

def home(request):
    return render(request, 'commissions/home.html')