from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CreateProjectView, ImageUploadViewSet


router = DefaultRouter()
router.register(r'projects/(?P<project_id>\d+)/images', ImageUploadViewSet, basename='images-view-set')


urlpatterns = [
    path('projects/', CreateProjectView.as_view(), name='create-project'),
    path('', include(router.urls)),
]
