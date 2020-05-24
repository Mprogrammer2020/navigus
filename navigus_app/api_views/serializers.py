from django.contrib.auth.models import User

from rest_framework import serializers
from api_views.models import TimeSlots, Bookings

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password')
        
class TimeSlotsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TimeSlots
        fields = ('id', 'teacher', 'dayDate', 'startTime', 'endTime', 'status')
        
class BookingsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Bookings
        fields = ('id', 'student', 'timeSlot')