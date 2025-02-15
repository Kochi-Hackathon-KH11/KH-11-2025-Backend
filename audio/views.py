from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import bad_request
from rest_framework.parsers import MultiPartParser, FormParser
import os

from utils.whisper import test_file
from django.conf import settings

class AudioUploadView(APIView):
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser)
    
    
    def post(self, request):
        file_obj = request.FILES.get('audio-file')
        if not file_obj.name.endswith('.mp3'):
            return bad_request()
        
        save_path = os.path.join(settings.BASE_DIR, 'media', file_obj.name)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

    
        with open(save_path, "wb+") as destination:
            for chunk in file_obj.chunks():
                destination.write(chunk)
        
        output = test_file(save_path)
    
        return Response({ 'message': output['text']})