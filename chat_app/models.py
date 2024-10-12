from django.db import models
from django.contrib.auth.models import User
from django_softdelete.models import SoftDeleteModel

class DefaultColumns(SoftDeleteModel):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    date_updated = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

# Create your models here.
class Conversation(DefaultColumns):
    DELIVERED = "DELIVERED"
    RECEIVED = "RECEIVED"
    STATUS_CHOICES = [
        (DELIVERED, "Delivered"),
        (RECEIVED, "Received"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')
    message = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=RECEIVED)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        ordering = ['-timestamp']
