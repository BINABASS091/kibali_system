from rest_framework import serializers
from django.contrib.auth.models import User
from .models import KibaliUser, Permit


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class KibaliUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = KibaliUser
        fields = ['id', 'user', 'role', 'created_at']


class PermitSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Permit
        fields = [
            'id',
            'permit_number',
            'created_by',
            'created_by_username',
            'jina',
            'aina',
            'pahala',
            'shehia',
            'kaskazini',
            'mashariki',
            'magharibi',
            'kusini',
            'upana',
            'urefu',
            'tarehe_kutolewa',
            'tarehe_mwisho',
            'pdf_file',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['permit_number', 'created_by', 'created_by_username', 'tarehe_kutolewa', 'pdf_file', 'created_at', 'updated_at']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
