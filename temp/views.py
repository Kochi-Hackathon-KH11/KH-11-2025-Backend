from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from utils.tts import text_to_speech
class HelloWorld(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        print(text_to_speech("hello what is your name"))
        return Response({ 'message': "hello-world" })