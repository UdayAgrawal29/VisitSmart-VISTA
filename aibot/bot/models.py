from django.db import models
from django.contrib.auth.models import AbstractUser

class Login(AbstractUser):
    # Inherit from Django's built-in User model to add custom fields
    booking_id = models.PositiveBigIntegerField(unique=True, blank=True, default=1000)

    def save(self, *args, **kwargs):
        if not self.booking_id or self.booking_id == 1000:  # Ensures no conflict
            # Get the last booking_id in the database or set to 1000 if no records exist
            last_id = Login.objects.order_by('-booking_id').first()
            self.booking_id = last_id.booking_id + 1 if last_id else 1000
        super(Login, self).save(*args, **kwargs)

    def __str__(self):
        return self.username

class Museum(models.Model):
    name = models.CharField(max_length=255)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=200)
    
    # Opening and closing times
    opening_time = models.TimeField(default="09:00")
    closing_time = models.TimeField(default="18:00")

    # Seats and queue for each hourly slot (9:00 to 18:00)
    slot_9_to_10_seats = models.PositiveIntegerField(default=100,blank=False)
    slot_9_to_10_queue = models.PositiveIntegerField(default=0,blank=False)
    slot_10_to_11_seats = models.PositiveIntegerField(default=100,blank=False)
    slot_10_to_11_queue = models.PositiveIntegerField(default=0,blank=False)
    slot_11_to_12_seats = models.PositiveIntegerField(default=100,blank=False)
    slot_11_to_12_queue = models.PositiveIntegerField(default=0,blank=False)
    slot_12_to_13_seats = models.PositiveIntegerField(default=100,blank=False)
    slot_12_to_13_queue = models.PositiveIntegerField(default=0,blank=False)
    slot_13_to_14_seats = models.PositiveIntegerField(default=100,blank=False)
    slot_13_to_14_queue = models.PositiveIntegerField(default=0,blank=False)
    slot_14_to_15_seats = models.PositiveIntegerField(default=100,blank=False)
    slot_14_to_15_queue = models.PositiveIntegerField(default=0,blank=False)
    slot_15_to_16_seats = models.PositiveIntegerField(default=100,blank=False)
    slot_15_to_16_queue = models.PositiveIntegerField(default=0,blank=False)
    slot_16_to_17_seats = models.PositiveIntegerField(default=100,blank=False)
    slot_16_to_17_queue = models.PositiveIntegerField(default=0,blank=False)
    slot_17_to_18_seats = models.PositiveIntegerField(default=100,blank=False)
    slot_17_to_18_queue = models.PositiveIntegerField(default=0,blank=False)

    # New fields
    zone = models.CharField(max_length=100, blank=True, null=True)
    weblinks = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
    
from django.db import models
from django.utils import timezone

from django.db import models
from django.utils import timezone

from django.db import models

class Transaction(models.Model):
    # Define the fields
    username = models.CharField(max_length=150, default='default_username')  # Renamed from 'name'
    booking_id = models.AutoField(primary_key=True)
    no_of_tickets = models.PositiveIntegerField(default=0)  # Total number of tickets booked
    booking_status = models.CharField(
        max_length=20, 
        choices=[('confirmed', 'Confirmed'), ('pending', 'Pending')],
        default='pending'
    )
    payment_status = models.CharField(
        max_length=20, 
        choices=[('paid', 'Paid'), ('unpaid', 'Unpaid')],
        default='unpaid'
    )
    slot = models.CharField(max_length=100, blank=True, null=True)  # Time slot for the booking
    date = models.DateField()  # Date of the booking
    waiting_list = models.PositiveIntegerField(default=0)  # Placeholder for waiting list count
    ticket_pdf = models.FileField(upload_to='tickets/', null=True, blank=True)  # Field for storing PDF tickets
    museum_name_id = models.CharField(max_length=255, default='')  # Museum name or ID
    
    # Fields for each slot with a default value of 100 tickets available
    s1 = models.PositiveIntegerField(default=100)  # Tickets available for Slot S1
    s2 = models.PositiveIntegerField(default=100)  # Tickets available for Slot S2
    s3 = models.PositiveIntegerField(default=100)
    s4 = models.PositiveIntegerField(default=100)
    s5 = models.PositiveIntegerField(default=100)
    s6 = models.PositiveIntegerField(default=100)  # Tickets available for Slot S3
    s7 = models.PositiveIntegerField(default=100)
    s8 = models.PositiveIntegerField(default=100)
    s9 = models.PositiveIntegerField(default=100)
    # Additional slots can be defined similarly
    # slot_s4_tickets = models.PositiveIntegerField(default=100)
    # slot_s5_tickets = models.PositiveIntegerField(default=100)

    def __str__(self):
        return f"Booking ID: {self.booking_id} - Username: {self.username} - Slot: {self.slot}"

    class Meta:
        ordering = ['date']

from django.db import models

class Bookings(models.Model):
    museum_name = models.CharField(max_length=250)
    # Use AutoField to automatically generate unique IDs
    id = models.AutoField(primary_key=True)  # AutoField generates IDs automatically
    date = models.DateField()
    
    # Slots for booking
    slot_9_to_10_seats = models.PositiveIntegerField(default=100, blank=False)
    slot_9_to_10_queue = models.PositiveIntegerField(default=0, blank=False)
    slot_10_to_11_seats = models.PositiveIntegerField(default=100, blank=False)
    slot_10_to_11_queue = models.PositiveIntegerField(default=0, blank=False)
    slot_11_to_12_seats = models.PositiveIntegerField(default=100, blank=False)
    slot_11_to_12_queue = models.PositiveIntegerField(default=0, blank=False)
    slot_12_to_13_seats = models.PositiveIntegerField(default=100, blank=False)
    slot_12_to_13_queue = models.PositiveIntegerField(default=0, blank=False)
    slot_13_to_14_seats = models.PositiveIntegerField(default=100, blank=False)
    slot_13_to_14_queue = models.PositiveIntegerField(default=0, blank=False)
    slot_14_to_15_seats = models.PositiveIntegerField(default=100, blank=False)
    slot_14_to_15_queue = models.PositiveIntegerField(default=0, blank=False)
    slot_15_to_16_seats = models.PositiveIntegerField(default=100, blank=False)
    slot_15_to_16_queue = models.PositiveIntegerField(default=0, blank=False)
    slot_16_to_17_seats = models.PositiveIntegerField(default=100, blank=False)
    slot_16_to_17_queue = models.PositiveIntegerField(default=0, blank=False)
    slot_17_to_18_seats = models.PositiveIntegerField(default=100, blank=False)
    slot_17_to_18_queue = models.PositiveIntegerField(default=0, blank=False)
