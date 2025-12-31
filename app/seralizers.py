from rest_framework import serializers
from . import models
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()

class SampleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SampleModel
        fields = ['id', 'name']
        
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    role=serializers.ChoiceField(choices=User.ROLE_CHOICES)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'password', 'confirm_password']
        
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return attrs  # 🔥 MUST RETURN

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)