import ffmpeg
import uuid
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from .models import WatermarkedVideo
from .forms import WatermarkForm


def watermark_video_view(request):
    if request.method == 'POST':
        form = WatermarkForm(request.POST, request.FILES)
        if form.is_valid():
            video_file = request.FILES['video']
            watermark_image_file = request.FILES['watermark_image']
            watermark_position = form.cleaned_data['watermark_position']
            watermark_size = form.cleaned_data['watermark_size']
            padding = form.cleaned_data['padding']

            video_filename = video_file.name
            watermark_filename = watermark_image_file.name

            # Save the files to the MEDIA_ROOT
            video_path = default_storage.save(f"videos/{video_filename}", ContentFile(video_file.read()))
            watermark_path = default_storage.save(f"watermarks/{watermark_filename}",
                                                  ContentFile(watermark_image_file.read()))

            id = uuid.uuid4()
            output_filename = f"{id}-watermarked_{video_file.name}"
            output_filepath = default_storage.path(f"watermarked_videos/{output_filename}")

            try:
                probe = ffmpeg.probe(default_storage.path(video_path))
                video_streams = [stream for stream in probe['streams'] if stream['codec_type'] == 'video']
                video_width = int(video_streams[0]['width'])
                video_height = int(video_streams[0]['height'])

                watermark_width = watermark_size

                # Probe the watermark to get its original dimensions
                watermark_info = ffmpeg.probe(default_storage.path(watermark_path))
                watermark_original_width = int(watermark_info['streams'][0]['width'])
                watermark_original_height = int(watermark_info['streams'][0]['height'])

                # Calculate the new height of the watermark while maintaining aspect ratio
                watermark_height = int((watermark_original_height / watermark_original_width) * watermark_width)

            except ffmpeg.Error as e:
                return HttpResponseBadRequest("An error occurred while probing the video.")

            # Map the position keyword to FFmpeg overlay filter parameters
            position_mappings = {
                'top-left': (padding, padding),
                'top-right': (video_width - watermark_width - padding, padding),
                'bottom-left': (padding, video_height - watermark_height - padding),
                'bottom-right': (video_width - watermark_width - padding, video_height - watermark_height - padding),
                'center': ((video_width - watermark_width) // 2, (video_height - watermark_height) // 2),
            }

            overlay_x, overlay_y = position_mappings.get(watermark_position, (padding, padding))

            # Apply watermark using ffmpeg
            try:
                in_video = ffmpeg.input(default_storage.path(video_path))
                watermark = ffmpeg.input(default_storage.path(watermark_path)).filter('scale', watermark_width,
                                                                                      watermark_height)

                has_audio = any(stream['codec_type'] == 'audio' for stream in probe['streams'])
                overlay_video = ffmpeg.overlay(in_video['v'], watermark, x=overlay_x, y=overlay_y)

                # Output file with both video and audio from the input
                if has_audio:
                    # Output file with both video and audio from the input
                    output = ffmpeg.output(overlay_video, in_video['a'], output_filepath, vcodec='libx264',
                                           acodec='copy', format='mp4')
                else:
                    # Output file with only video
                    output = ffmpeg.output(overlay_video, output_filepath, vcodec='libx264', format='mp4')
                output.overwrite_output().run()

            except ffmpeg.Error as e:
                default_storage.delete(video_path)
                default_storage.delete(watermark_path)
                return HttpResponseBadRequest("An error occurred while applying the watermark.")

            # Store information in the database
            new_video = WatermarkedVideo(
                user=request.user,
                video='watermarked_videos/' + output_filename,
                watermark_image='watermarks/' + watermark_filename,
                watermark_position=watermark_position,
                watermark_size=watermark_size,
                padding=padding,
            )
            new_video.save()

            # Generate the URL for the watermarked video
            video_url = request.build_absolute_uri(settings.MEDIA_URL + f"watermarked_videos/{output_filename}")

            return JsonResponse({'video_url': video_url})
    else:
        form = WatermarkForm()

    return render(request, '../templates/watermark.html', {'form': form})
