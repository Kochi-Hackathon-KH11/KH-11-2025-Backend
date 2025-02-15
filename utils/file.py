import os
from django.conf import settings
import io
import soundfile as sf    
from pydub import AudioSegment

def save_audio_file(file):
    save_path = os.path.join(settings.BASE_DIR, 'media', file.name)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    with open(save_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
            
    return save_path


def buffer_to_audio(data):
    waveform = data['audio']
    sampling_rate = data['sampling_rate']
    
    wav_buffer = io.BytesIO()
    sf.write(wav_buffer, waveform, samplerate=sampling_rate, format='WAV')
    wav_buffer.seek(0)
    
    
    audio = AudioSegment.from_wav(wav_buffer)
    mp3_buffer = io.BytesIO()
    audio.export(mp3_buffer, format='mp3', bitrate='128k')
    mp3_buffer.seek(0)
    
    return mp3_buffer    
