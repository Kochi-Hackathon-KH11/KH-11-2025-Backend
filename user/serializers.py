from rest_framework import serializers
from django.contrib.auth.models import User
from .models import CallHistory

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=0)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class CallHistorySerializer(serializers.ModelSerializer):
    receiver_name = serializers.SerializerMethodField()

    class Meta:
        model = CallHistory
        fields = ('receiver_name', 'duration', 'accepted', 'time')

    def get_receiver_name(self, obj):
        return obj.receiver.username