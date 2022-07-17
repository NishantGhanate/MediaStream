# Generated by Django 4.0.5 on 2022-07-16 18:33

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import video_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('video_app', '0002_generemodel_categorymodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('title_slug', models.SlugField(blank=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('video_file_path', models.FileField(upload_to=video_app.models.USER_DIRECTORY_PATH, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp4'])])),
                ('m3u8_file_path', models.CharField(blank=True, max_length=255)),
                ('thumbnail', models.ImageField(upload_to=video_app.models.USER_DIRECTORY_PATH, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])),
                ('released_date', models.DateField(blank=True, null=True)),
                ('uploaded_date', models.DateTimeField(auto_now_add=True)),
                ('processing_status', models.IntegerField(choices=[(-1, 'Failed'), (0, 'Queued'), (1, 'Started'), (2, 'Finished')], default=0)),
                ('processing_completed', models.DurationField(blank=True, null=True)),
                ('duration', models.DurationField(blank=True, null=True)),
                ('file_size', models.CharField(blank=True, max_length=15, null=True)),
                ('dimension', models.CharField(blank=True, max_length=15, null=True)),
                ('display_aspect_ratio', models.CharField(blank=True, max_length=10, null=True)),
                ('overall_bit_rate', models.CharField(blank=True, max_length=15, null=True)),
                ('video_bitrate', models.CharField(blank=True, max_length=15, null=True)),
                ('audio_bitrate', models.CharField(blank=True, max_length=15, null=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='video_app.categorymodel')),
                ('genre_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='video_app.generemodel')),
            ],
        ),
    ]
