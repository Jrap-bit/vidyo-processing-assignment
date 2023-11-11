from django.db import models
from django.contrib.auth.models import User


class AudioExtraction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    audio = models.FileField(upload_to='audios/', null=True)
    extraction_timestamp = models.DateTimeField(auto_now_add=True)
    audio_duration = models.FloatField(null=True, blank=True)
