from django.contrib import admin
from .models import AudioExtraction

@admin.register(AudioExtraction)
class AudioExtractionAdmin(admin.ModelAdmin):
    list_display = ('user', 'audio', 'extraction_timestamp', 'audio_duration')
    list_filter = ('extraction_timestamp',)
    search_fields = ('user__username',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
