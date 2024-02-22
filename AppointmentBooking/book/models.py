from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class TimeSlot(BaseModel):
    start_time = models.TimeField(unique=True)
    end_time = models.TimeField()

    def __str__(self):
        return f'{self.start_time} - {self.end_time}'
    
class Appointment(BaseModel):
    booked_at = models.DateField()
    booked_by = models.ForeignKey(User, on_delete=models.CASCADE)
    booked_for = models.ForeignKey(User, on_delete=models.CASCADE, related_name='booked_for')
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    booked = models.CharField(max_length=100, default='Available')

    def __str__(self):
        return f'{self.booked_by} - {self.booked_for} - {self.time_slot} - {self.booked_at}'