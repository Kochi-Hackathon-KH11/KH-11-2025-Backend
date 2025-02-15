from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, APIException
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from utils.whisper import speech_to_text_from_file
from utils.file import save_audio_file, buffer_to_audio
from utils.tts import text_to_speech
from rest_framework import status
class AudioUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [AllowAny]
    
    def post(self, request):
        file_obj = request.FILES.get('audio-file')
        if not file_obj.name.endswith('.mp3') and not file_obj.name.endswith('.wav'):
            raise ValidationError()
        
        output_path = save_audio_file(file_obj)
        
        text = speech_to_text_from_file(output_path)
        if text is None:
            raise APIException()
        
        speech = text_to_speech(text)
        mp3_buffer = buffer_to_audio(speech)
        
        return Response(
            mp3_buffer.getvalue(),
            content_type="audio/mpeg",
            status=status.HTTP_200_OK,
            headers={"Content-Disposition": 'attachment; filename="output.mp3"'}
        )
    
    
# class AudioStreamView(APIView):
#     parser_classes = (MultiPartParser, FormParser)
#     permission_classes = [AllowAny]
    
#     def post(self, request):
#         file_obj = request.FILES.get('audio-file')
#         if not file_obj.name.endswith('.wav') or file_obj.name.endswith('.mp3'):
#             return bad_request()
        
#         audio_data = file_obj.read()
#         audio_stream = io.BytesIO(audio_data)
#         waveform, sample_rate = sf.read(audio_stream, dtype="float32")
        
#         transcript = 
              
