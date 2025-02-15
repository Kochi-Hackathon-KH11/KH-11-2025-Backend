import os
from django.conf import settings
import io
import soundfile as sf    
from pydub import AudioSegment

def save_audio_file(file):
    """
    Saves an uploaded audio file to the media directory.

    Args:
        file (InMemoryUploadedFile): The uploaded file object.

    Returns:
        str: The path where the file is saved.
    """
    
    
    save_path = os.path.join(settings.BASE_DIR, 'media', file.name)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    with open(save_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
            
    return save_path

def save_webm_as_wav(file):
    """
    Converts a WebM audio file to WAV format with a sampling rate of 16kHz, mono channel, and 16-bit depth.

    Args:
        file (InMemoryUploadedFile): The uploaded WebM file.

    Returns:
        str: The path to the saved WAV file.
    """
    save_path = save_audio_file(file)
    audio = AudioSegment.from_file(save_path, format="webm")
    audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
    output_path = os.path.join(settings.BASE_DIR, 'media', 'output.wav')
    audio.export("media/output.wav", format="wav")
    delete_file(save_path)
    return output_path

def buffer_to_audio(data):
    """
    Converts an in-memory audio buffer into a WAV file and then exports it as an MP3 buffer.

    Args:
        data (dict): A dictionary containing:
            - 'audio' (numpy.ndarray): The waveform data.
            - 'sampling_rate' (int): The sampling rate of the audio.

    Returns:
        io.BytesIO: A buffer containing the MP3 audio data.
    """
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

def delete_file(path):
    """
    Deletes a file from the filesystem if it exists.

    Args:
        path (str): The file path to be deleted.

    Returns:
        bool: True if the file was deleted successfully, False if the file does not exist.
    """
    if os.path.exists(path) and os.path.isfile(path):
        os.remove(path)
        return True 
    return False