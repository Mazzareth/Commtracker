#!/usr/bin/env python
import os
import sys
import django
from datetime import date, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'commissions_tracker.settings')
django.setup()

from commissions.models import Commission

# Create sample commissions
sample_commissions = [
    {
        'title': 'Website Design for Local Restaurant',
        'description': 'Complete website redesign including menu integration and online ordering system.',
        'client_name': 'Mario\'s Italian Kitchen',
        'client_email': 'mario@italiankit.com',
        'amount': 2500.00,
        'status': 'in_progress',
        'due_date': date.today() + timedelta(days=14),
    },
    {
        'title': 'Logo Design for Startup',
        'description': 'Modern logo design for tech startup including brand guidelines.',
        'client_name': 'TechFlow Solutions',
        'client_email': 'contact@techflow.com',
        'amount': 800.00,
        'status': 'completed',
        'due_date': date.today() - timedelta(days=5),
        'completed_date': date.today() - timedelta(days=2),
    },
    {
        'title': 'Mobile App UI Design',
        'description': 'User interface design for fitness tracking mobile application.',
        'client_name': 'FitTrack Inc',
        'client_email': 'design@fittrack.app',
        'amount': 3200.00,
        'status': 'pending',
        'due_date': date.today() + timedelta(days=30),
    },
    {
        'title': 'E-commerce Platform Development',
        'description': 'Full e-commerce website with payment integration and inventory management.',
        'client_name': 'Artisan Crafts Co',
        'client_email': 'orders@artisancrafts.com',
        'amount': 5500.00,
        'status': 'in_progress',
        'due_date': date.today() + timedelta(days=45),
    },
    {
        'title': 'Business Card Design',
        'description': 'Professional business card design for law firm.',
        'client_name': 'Johnson & Associates Law',
        'client_email': 'info@johnsonlaw.com',
        'amount': 150.00,
        'status': 'completed',
        'completed_date': date.today() - timedelta(days=10),
    },
]

print("Creating sample commissions...")
for commission_data in sample_commissions:
    commission, created = Commission.objects.get_or_create(
        title=commission_data['title'],
        defaults=commission_data
    )
    if created:
        print(f"✓ Created: {commission.title}")
    else:
        print(f"- Already exists: {commission.title}")

print(f"\nTotal commissions in database: {Commission.objects.count()}")