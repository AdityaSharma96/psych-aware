from django.db import models
from accounts.models import Expert_Profile, Client_Profile
# Create your models here.

class Appointment(models.Model):
    appointment_id = models.AutoField(primary_key=True)
    client_profile = models.ForeignKey(to=Client_Profile, on_delete=models.CASCADE,null=True)
    expert_profile = models.ForeignKey(to=Expert_Profile, on_delete=models.CASCADE, null=True)
    datetime = models.DateTimeField(auto_now_add=False, null=True)
    client_acknowledgement = models.CharField(max_length=3, default='NA')
    expert_acknowledgement = models.CharField(max_length=3, default='NA')
    chat_room = models.CharField(max_length=100, default='NA')

    def __str__(self):
        return str(self.appointment_id) + " {} " + str(self.client_profile) + " -> " + str(self.expert_profile)
