# Generated by Django 4.2.4 on 2024-06-19 20:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='file',
            field=models.ImageField(null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='image',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='images', to='projects.project', verbose_name='Проект'),
        ),
    ]
