from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class TimeSlots(models.Model):
    id = models.BigAutoField(primary_key=True)
    teacher = models.ForeignKey(User, null="True", on_delete=models.CASCADE)
    dayDate = models.DateTimeField(null="True")
    startTime = models.CharField(max_length=255, default="")
    endTime = models.CharField(max_length=255, default="")
    status = models.IntegerField(default=1)#1 for available, 2 for booked

    class Meta:
        db_table = 'timeslots'
        permissions = (('can_view_time_slots', 'can view time slots')),
        
class Bookings(models.Model):
    id = models.BigAutoField(primary_key=True)
    student = models.ForeignKey(User, null="True", on_delete=models.CASCADE)
    timeSlot = models.ForeignKey(TimeSlots, null="True", on_delete=models.CASCADE)
    bookingTime = models.DateTimeField(null="True")
    
    class Meta:
        db_table = 'bookings'
        permissions = (('can_view_bookings', 'can view bookings')),