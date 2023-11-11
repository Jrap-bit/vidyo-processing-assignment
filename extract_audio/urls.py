from django.urls import path
from . import views


urlpatterns = [
    path('', views.extract_audio_view, name='extract_audio'),
]
