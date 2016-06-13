import bpy

def Settings():
    # MPEG
    for scene in bpy.data.scenes:
        scene.render.image_settings.file_format = 'H264'
        scene.render.ffmpeg.format = 'QUICKTIME'
        scene.render.image_settings.color_mode = 'RGB'
        scene.render.ffmpeg.audio_codec = 'AAC'
        scene.render.ffmpeg.audio_bitrate = 128
        scene.render.resolution_percentage = 100
