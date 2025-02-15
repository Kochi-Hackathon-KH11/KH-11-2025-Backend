from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from utils.datasets import get_sample
from utils.whisper import test_buffer
class HelloWorld(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        data = get_sample()
        output = test_buffer(data)
        print(output)
        return Response({ 'message': output })