from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        request = self.context.get('request')
        if request:
            login(request, user)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if user and user.is_active:
            data['user'] = user
        else:
            raise serializers.ValidationError('Invalid Credentials')
        return data

    def to_representation(self, instance):
        user = instance['user']
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
        }