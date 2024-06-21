from __future__ import annotations

from django.contrib import admin

from .models import Project, Image


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass
