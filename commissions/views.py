from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Commission, Client, Character
from .forms import ClientForm, CommissionForm, CharacterForm

def commission_list(request):
    commissions = Commission.objects.all()

    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        commissions = commissions.filter(
            Q(title__icontains=search_query) |
            Q(client__nickname__icontains=search_query) |
            Q(client__handle__icontains=search_query) |
            Q(client__email__icontains=search_query) |
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

# ----- Client Management -----

def client_list(request):
    clients = Client.objects.all().order_by('-created_at')
    return render(request, 'commissions/client_list.html', {'clients': clients})

def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save()
            messages.success(request, "Client created successfully.")
            return redirect('commissions:client_detail', pk=client.pk)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ClientForm()
    return render(request, 'commissions/client_form.html', {'form': form, 'form_title': 'Add Client'})

def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk)
    commissions = client.commissions.all()
    characters = client.characters.all()
    return render(request, 'commissions/client_detail.html', {
        'client': client,
        'commissions': commissions,
        'characters': characters,
    })

# ----- Add commission for client -----

def commission_create_for_client(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        form = CommissionForm(request.POST)
        if form.is_valid():
            commission = form.save(commit=False)
            commission.client = client
            commission.save()
            form.save_m2m()
            messages.success(request, "Commission created and assigned to client.")
            return redirect('commissions:commission_detail', pk=commission.pk)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CommissionForm()
    return render(request, 'commissions/commission_form.html', {
        'form': form,
        'form_title': f'Add Commission for {client.nickname}',
        'client': client,
        'hide_client_field': True,
    })

# ----- Add character for client -----

def character_create_for_client(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        form = CharacterForm(request.POST)
        if form.is_valid():
            character = form.save(commit=False)
            character.client = client
            character.save()
            messages.success(request, "Character created and assigned to client.")
            return redirect('commissions:client_detail', pk=client.pk)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CharacterForm()
    return render(request, 'commissions/character_form.html', {
        'form': form,
        'form_title': f'Add Character for {client.nickname}',
        'client': client,
        'hide_client_field': True,
    })