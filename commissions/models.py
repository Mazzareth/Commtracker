from django.db import models
from django.core.validators import MinValueValidator

class Commission(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    TYPE_CHOICES = [
        ('art', 'Art'),
        ('writing', 'Writing'),
        ('music', 'Music'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    client = models.ForeignKey(
        'Client', on_delete=models.CASCADE, related_name='commissions'
    )
    characters = models.ManyToManyField('Character', blank=True, related_name='commissions')
    tags = models.ManyToManyField('Tag', blank=True, related_name='commissions')
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='art')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateField(null=True, blank=True)
    completed_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def client_name(self):
        return self.client.nickname

    @property
    def client_email(self):
        return self.client.email