# Generated by Django 4.0.5 on 2022-07-29 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LanguageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('name_slug', models.SlugField(blank=True)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]