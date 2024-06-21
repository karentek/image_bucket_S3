from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from rest_framework.viewsets import ModelViewSet
from .service.quorisets import get_related_images

from .models import Project
from .serializers import ProjectSerializer, ImageSerializer, ImageCreateSerializer


class CreateProjectView(CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]


class ImageUploadViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        user_id = self.request.user.id
        return get_related_images(project_id, user_id)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return ImageSerializer
        if self.action == 'create':
            return ImageCreateSerializer
        return ImageSerializer
