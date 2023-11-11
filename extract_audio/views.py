import os
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
import ffmpeg
from .forms import VideoUploadForm
from .models import AudioExtraction
import magic
from django.http import HttpResponseBadRequest


def extract_audio_view(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video_file = request.FILES['video']

            # Check if the file is a video file
            mime = magic.from_buffer(video_file.read(2048), mime=True)
            if not mime.startswith('video'):
                return HttpResponseBadRequest("Invalid file type: Please upload a video file.")
            video_file.seek(0)

            # Check if the video file contains an audio stream
            try:
                metadata = ffmpeg.probe(video_file.temporary_file_path(), select_streams='a')
                if not metadata['streams']:
                    return HttpResponseBadRequest("The video does not contain an audio stream.")
            except ffmpeg.Error as e:
                return HttpResponseBadRequest("An error occurred while checking the video.")

            output_filename = os.path.splitext(video_file.name)[0] + '.mp3'
            output_filepath = os.path.join(settings.MEDIA_ROOT, 'audios', output_filename)

            # Extract Audio
            ffmpeg.input(video_file.temporary_file_path()).output(output_filepath).run()

            # Get Audio Duration
            metadata = ffmpeg.probe(output_filepath, select_streams='a')
            audio_duration = float(metadata['streams'][0]['duration'])

            # Save the audio metadata
            extraction = AudioExtraction()
            if request.user.is_authenticated:
                extraction.user = request.user
            extraction.audio_duration = audio_duration
            extraction.audio.name = os.path.join('audios', output_filename)
            extraction.save()

            # Return Audio URL
            audio_file_url = request.build_absolute_uri(settings.MEDIA_URL + 'audios/' + output_filename)

            return JsonResponse({'audio_url': audio_file_url})
    else:
        form = VideoUploadForm()

    return render(request, '../templates/upload.html', {'form': form})
