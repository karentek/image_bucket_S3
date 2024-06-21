from django.db import models

from django.contrib.auth.models import User
from .service.resize import resize_image


class Project(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Название',

    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='projects',
        verbose_name='Пользователь',

    )

    def str(self):
        return self.name


class Status(models.TextChoices):
    INITIAL = 'INITIAL', 'Инициализировано'
    UPLOADED = 'UPLOADED', 'Загружено'
    PROCESSING = 'PROCESSING', 'В процессе'
    DONE = 'DONE', 'Готово'
    ERROR = 'ERROR', 'Ошибка'


class Image(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.PROTECT,
        related_name='images',
        verbose_name='Проект',
    )
    file = models.ImageField(
        null=True
    )
    filename = models.CharField(
        max_length=255,
        verbose_name='Название файла',
    )
    state = models.CharField(
        verbose_name='Статус',
        choices=Status.choices,
        db_index=True,
        default=Status.INITIAL,
    )

    original = models.ImageField(
        blank=True,
        null=True,
        verbose_name='Оригинал',
    )

    thumb = models.ImageField(
        blank=True,
        null=True,
    )
    big_thumb = models.ImageField(
        blank=True,
        null=True
    )
    big_1920 = models.ImageField(
        blank=True,
        null=True
    )
    d2500 = models.ImageField(
        blank=True,
        null=True
    )

    def str(self):
        return self.filename

    def save(self, *args, save_model=True, **kwargs):
        if self.original:
            self.state = 'PROCESSING'
            self.thumb = resize_image(self.original, 120, 150)
            self.big_thumb = resize_image(self.original, 700, 700)
            self.big_1920 = resize_image(self.original, 1080, 1920)
            self.d2500 = resize_image(self.original, 2500, 2500)
            self.state = 'DONE'
        return super().save(*args, **kwargs)