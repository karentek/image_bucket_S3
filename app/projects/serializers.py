from rest_framework import serializers
from .models import Image, Project


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = [
            'name',
            'description'
        ]

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        project = Project.objects.create(
            user=user,
            description=validated_data['description'],
            name=validated_data['name']
        )
        return project


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class ImageCreateSerializer(serializers.ModelSerializer):
    file = serializers.ImageField(write_only=True)

    class Meta:
        model = Image
        fields = [
            'filename',
            'file',
            'project',
        ]

    def create(self, validated_data):
        image = validated_data.pop('file')
        instance = super().create(validated_data)
        instance.original = image
        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['original'] = instance.original.url
        return representation




