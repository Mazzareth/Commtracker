from django.db import models
from django.core.validators import MinValueValidator

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
    client = models.ForeignKey(Client, related_name='characters', on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(blank=True)
    reference_url = models.URLField(blank=True)  # Deprecated - for migration only
    reference_file = models.ImageField(upload_to='character_references/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.client.nickname})"

class ClientNote(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='client_notes')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class CommissionNote(models.Model):
    commission = models.ForeignKey(Commission, on_delete=models.CASCADE, related_name='commission_notes')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Note for {self.commission.title} ({self.created_at})"

class Tag(models.Model):
    """Tags for categorizing commissions (e.g. Swimming, 2 Character, etc)."""
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Commission(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    TYPE_CHOICES = [
        ('sketch', 'Sketch'),
        ('animation', 'Animation'),
        ('full', 'Full Illustration'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    client = models.ForeignKey(Client, related_name='commissions', on_delete=models.CASCADE, null=True, blank=True)
    characters = models.ManyToManyField(Character, related_name='commissions', blank=True)
    tags = models.ManyToManyField(Tag, related_name='commissions', blank=True)
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='sketch')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateField(null=True, blank=True)
    completed_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.title} - {self.client.nickname} (${self.amount})"

    @property
    def client_name(self):
        return self.client.nickname

    @property
    def client_email(self):
        return self.client.email

    class Meta:
        ordering = ['-created_at']