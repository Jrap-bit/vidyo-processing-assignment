from django.db import models
from django.contrib.auth.models import User


class WatermarkedVideo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    video = models.FileField(upload_to='watermarked_videos/')
    watermark_image = models.ImageField(upload_to='watermarks/')
    watermark_position = models.CharField(max_length=100)
    watermark_size = models.IntegerField(default=100, null=True, blank=True)
    padding = models.IntegerField(default=10, null=True, blank=True)
    processed_time = models.DateTimeField(auto_now_add=True)
