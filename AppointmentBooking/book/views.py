from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import TimeSlot, Appointment
from .serializers import CreateUserSerializer, TimeSlotSerializer, BookAppointmentSerializer, UpdateAppointmentSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import mixins
from .permissions import IsOwnerOrReadOnly
from rest_framework import generics
# Create your views here.

class CreateUserView(APIView):
    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            response_data = {
                                'refresh': str(refresh),
                                'access': str(refresh.access_token),
                            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateTimeSlotView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly,]

    def post(self, request):
        serializer = TimeSlotSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request,pk):
        time_slot = TimeSlot.objects.filter(pk=pk).first()
        if time_slot:
            time_slot.delete()
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)

class BookAppointmentView(generics.GenericAPIView, mixins.DestroyModelMixin,APIView, mixins.UpdateModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly,]
    queryset = Appointment.objects.all()
    serializer_class = BookAppointmentSerializer

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return UpdateAppointmentSerializer
        return BookAppointmentSerializer

    def post(self, request):
        data = request.data
        time_slot = TimeSlot.objects.filter(id= data['time_slot']).first()
        if not time_slot:
            return Response({'error':'Invalid Time Slot'}, status=status.HTTP_400_BAD_REQUEST)
        appointment = Appointment.objects.filter(time_slot=time_slot, booked_at=data['booked_at'], booked_for = data['booked_for']).first()
        if appointment:
            return Response({'error':'Time Slot already booked'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = BookAppointmentSerializer(data=data)

        if serializer.is_valid():
            serializer.save(booked_by=request.user,booked = 'Booked')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
    def get(self, request):
        appointments = Appointment.objects.filter(booked_by=request.user)
        serializer = BookAppointmentSerializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


        
class CheckAvailabilityView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = request.data
        serializer = Appointment.objects.filter(booked_for= data['booked_for'], booked='Booked', booked_at=data['booked_at'])
        time = []
        for val in serializer:
            time.append(val.time_slot.pk)
        
        time_slots = TimeSlot.objects.all()
        available = []
        for slot in time_slots:
            if slot.pk not in time:
                available.append({"slot": slot.pk, "start_time": slot.start_time, "end_time": slot.end_time})
        return Response(available, status=status.HTTP_200_OK)