from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegisterSerializer, CallHistorySerializer
from .models import CallHistory
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
class RegisterView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.save()
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            },
            'token': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }
        })
        
        
class CallHistoryView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CallHistorySerializer
        
    def get_queryset(self):
        user = self.request.user
        return CallHistory.objects.filter(sender=user) | CallHistory.objects.filter(receiver=user)
    