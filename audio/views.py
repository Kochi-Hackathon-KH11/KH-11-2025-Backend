from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, APIException
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from utils.whisper import speech_to_text_from_file
from utils.file import save_audio_file, buffer_to_audio, save_webm_as_wav
from utils.tts import text_to_speech
from rest_framework import status
from django.http import FileResponse, StreamingHttpResponse
import io 
import soundfile as sf
from pydub import AudioSegment
class AudioUploadView(APIView):
    """Cleans audio and gives output as an mp3 file
    """
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [AllowAny]
    
    def post(self, request):
        file_obj = request.FILES.get('audio-file')
        if file_obj.name.endswith('.webm'):
            output_path = save_webm_as_wav(file_obj)
        elif not file_obj.name.endswith('.mp3') and not file_obj.name.endswith('.wav'):
            raise ValidationError()
        else:
            output_path = save_audio_file(file_obj)
        
        text = speech_to_text_from_file(output_path)
        
        speech = text_to_speech(text)
        mp3_buffer = buffer_to_audio(speech)
        
        response = FileResponse(mp3_buffer, content_type="audio/mpeg")
        response["Content-Disposition"] = 'attachment; filename="output.mp3"'
        
        return response
    
class AudioStreamView(APIView):
    """Cleans audio and returns output in the form of a streaming response
    """
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [AllowAny]
    
    def post(self, request):
        file_obj = request.FILES.get('audio-file')
        if file_obj.name.endswith('.webm'):
            output_path = save_webm_as_wav(file_obj)
        elif not file_obj.name.endswith('.mp3') and not file_obj.name.endswith('.wav'):
            raise ValidationError()
        else:
            output_path = save_audio_file(file_obj)
        
        output_path = save_audio_file(file_obj)
        
        text = speech_to_text_from_file(output_path)
        
        speech = text_to_speech(text)
        mp3_buffer = buffer_to_audio(speech)
        
        response = StreamingHttpResponse(mp3_buffer, content_type='audio/mpeg')    
        response["Content-Disposition"] = 'inline; filename="output.mp3"'
        return response
        
        
              
