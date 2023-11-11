from django.contrib import admin
from .models import WatermarkedVideo


@admin.register(WatermarkedVideo)
class WatermarkedVideoAdmin(admin.ModelAdmin):
    list_display = ['user', 'processed_time', 'video', 'watermark_image', 'watermark_position']
