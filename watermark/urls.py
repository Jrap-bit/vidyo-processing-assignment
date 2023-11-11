from django.urls import path
from .views import watermark_video_view

urlpatterns = [
    path('', watermark_video_view, name='watermark_video'),
]
