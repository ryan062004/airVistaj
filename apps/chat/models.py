from django.db import models
from django.utils import timezone

class ChatMessage(models.Model):
    username = models.CharField(max_length=150)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username}: {self.message[:20]}"