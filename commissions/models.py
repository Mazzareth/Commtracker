from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class Client(models.Model):
    """A client/customer in the CRM."""
    nickname = models.CharField(max_length=100, unique=True, help_text="Display nickname for the client.")
    handle = models.CharField(max_length=100, unique=True, help_text="Unique handle (like @user) for the client.")
    email = models.EmailField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nickname} ({self.handle})"

class Character(models.Model):
    """A character (OC) belonging to a client."""
    name = models.CharField(max_length=100)
    client = models.ForeignKey(Client, related_name='characters', on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    reference_url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.client.nickname})"

class Tag(models.Model):
    """Tags for categorizing commissions (e.g. Swimming, 2 Character, etc)."""
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Commission(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def client_name(self):
        return self.client.nickname

    @property
    def client_email(self):
        return self.client.email
    due_date = models.DateField(null=True, blank=True)
    completed_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.client.nickname} (${self.amount})"