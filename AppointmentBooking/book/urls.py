from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', CreateUserView.as_view(), name='register'),
    path('create_time_slot/', CreateTimeSlotView.as_view(), name='create_time_slot'),
    path('delete_time_slot/<int:pk>/', CreateTimeSlotView.as_view(), name='delete_time_slot'),
    path('book_appointment/', BookAppointmentView.as_view(), name='book_appointment'),
    path('delete_appointment/<int:pk>/', BookAppointmentView.as_view(), name='delete_appointment'),
    path('get_appointments/', BookAppointmentView.as_view(), name='get_appointments'),
    path('check_availability/', CheckAvailabilityView.as_view(), name='check_availability'),
    path('update_appointment/<int:pk>/', BookAppointmentView.as_view(), name='update_appointment'),

]