from celery import shared_task
from .models import Image
import boto3
from django.conf import settings
from django.core.files.base import ContentFile
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@shared_task
def add(x, y):
    return x + y

    # image = Image.objects.get(id=image_id)
    # # Загрузка изображения с S3
    # s3_client = boto3.client(
    #     's3',
    #     region_name=settings.AWS_S3_REGION_NAME,
    #     endpoint_url=settings.AWS_S3_ENDPOINT_URL,
    #     aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    #     aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    # )
    #
    # key = image.original.name
    # temp_file = NamedTemporaryFile(delete=False)
    #
    # s3_client.download_fileobj(settings.AWS_STORAGE_BUCKET_NAME, key, temp_file)
    #
    # # Обработка изображения
    # temp_file.seek(0)
    # processed_image = resize_image(temp_file, 120, 150)
    #
    # # Загрузка обработанных изображений обратно на S3
    # s3_client.upload_fileobj(processed_image, settings.AWS_STORAGE_BUCKET_NAME,
    #                          f'project_{image.project.id}/thumb/{image.filename}')
    #
    # image.thumb = f'https://{settings.AWS_STORAGE_BUCKET_NAME}.storage.yandexcloud.net/project_{image.project.id}/thumb/{image.filename}'
    # image.state = 'DONE'
    # image.save()
    #
    # # Уведомление через WebSocket
    # channel_layer = get_channel_layer()
    # async_to_sync(channel_layer.group_send)(
    #     f'user_{image.project.user.id}',
    #     {
    #         'type': 'send_notification',
    #         'message': {'status': 'Image processing done', 'image_id': image.id}
    #     }
    # )