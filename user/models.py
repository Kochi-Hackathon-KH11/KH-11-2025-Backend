from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class CallHistory(models.Model):
    sender = models.ForeignKey(User, related_name='sent_calls', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_calls', on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} -> {self.receiver} ({'Accepted' if self.accepted else 'Missed'})"