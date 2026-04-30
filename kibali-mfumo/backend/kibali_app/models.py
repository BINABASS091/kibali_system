from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class KibaliUser(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('officer', 'Officer'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='officer')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"


class Permit(models.Model):
    CONSTRUCTION_TYPES = [
        ('UKUTA', 'Ukuta (Wall)'),
        ('NYUMBA', 'Nyumba (House)'),
        ('JENGO', 'Jengo (Building)'),
        ('KIWANDA', 'Kiwanda (Factory)'),
        ('DUKA', 'Duka (Shop)'),
        ('OFISI', 'Ofisi (Office)'),
    ]
    
    # Permit number (auto-generated)
    permit_number = models.CharField(max_length=20, unique=True)
    
    # User who created this permit
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    # Permit form fields
    jina = models.CharField(max_length=255)  # Name of applicant
    aina = models.CharField(max_length=50, choices=CONSTRUCTION_TYPES)  # Type of construction
    pahala = models.CharField(max_length=255)  # Location
    shehia = models.CharField(max_length=255)  # Ward/Parish
    
    # Land boundaries
    kaskazini = models.CharField(max_length=255)  # North
    mashariki = models.CharField(max_length=255)  # East
    magharibi = models.CharField(max_length=255)  # West
    kusini = models.CharField(max_length=255)  # South
    
    # Measurements
    upana = models.FloatField()  # Width in meters
    urefu = models.FloatField()  # Height/Length in meters
    
    # Dates
    tarehe_kutolewa = models.DateField(auto_now_add=True)  # Issue date
    tarehe_mwisho = models.DateField()  # Expiry date
    
    # PDF file
    pdf_file = models.FileField(upload_to='permits/', blank=True, null=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.permit_number} - {self.jina}"
    
    def save(self, *args, **kwargs):
        if not self.permit_number:
            # Generate permit number
            last_permit = Permit.objects.all().order_by('-id').first()
            if last_permit and last_permit.permit_number:
                try:
                    number = int(last_permit.permit_number.split('-')[1]) + 1
                except:
                    number = 1
            else:
                number = 1
            self.permit_number = f"KU-{number:04d}"
        
        super().save(*args, **kwargs)
