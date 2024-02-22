from rest_framework.serializers import ModelSerializer
from django.contrib.auth.hashers import make_password
from .models import TimeSlot, Appointment
from .views import *
from django.contrib.auth.models import User
from rest_framework import serializers

class CreateUserSerializer(ModelSerializer):
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = User.objects.create(**validated_data)

        return user
        
    class Meta:
        model = User
        fields = ['username','password']

class TimeSlotSerializer(ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ['start_time','end_time']

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class BookAppointmentSerializer(ModelSerializer):
    booked_for = UserSerializer()
    time_slot = TimeSlotSerializer()
    class Meta:
        model = Appointment
        fields = ['booked_at','booked_for','time_slot']


class UpdateAppointmentSerializer(ModelSerializer):
    
    def update(self, instance, validated_data):

        instance.booked_by = validated_data.get('booked_by', instance.booked_by)
        instance.booked_for = validated_data.get('booked_for', instance.booked_for)
        instance.time_slot = validated_data.get('time_slot', instance.time_slot)
        instance.booked_at = validated_data.get('booked_at', instance.booked_at)
        instance.save()
        return instance
    class Meta:
        model = Appointment
        fields = ['booked','booked_at','booked_for','time_slot',]


