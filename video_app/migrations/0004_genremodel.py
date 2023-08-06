# Generated by Django 4.1.10 on 2023-08-06 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video_app', '0003_languagemodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenreModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('name_slug', models.SlugField(blank=True)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]