import logging
import traceback

from os import sep as os_slash
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from django.utils import timezone
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator


from video_app.managers import CustomUserManager, GetOrNoneManager

logger = logging.getLogger('video_app')

def USER_DIRECTORY_PATH(instance, file_name):
    try:
        return os_slash.join([
            instance.category.name,
            instance.category.lang,
            instance.title_slug,
            file_name
        ])
    except :
        logger.error(traceback.format_exc())
    
class CustomUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField('email address', unique=True)
    is_staff = models.BooleanField(default= False)
    is_active = models.BooleanField(default= False)
    date_joined = models.DateTimeField(default= timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class CategoryModel(models.Model):
    name = models.CharField(max_length= 50, null=False, blank=False)
    lang = models.CharField(max_length= 50, null=False, blank=False)
    objects = GetOrNoneManager()

    class Meta:
        unique_together = ('name', 'lang',)

    def __str__(self):
        return '{} - {}'.format(self.lang, self.name)

class GenereModel(models.Model):
    type = models.CharField(max_length= 100)

    def __str__(self):
        return f'{self.type}'

class Status(models.IntegerChoices):
    FAILED = -1
    QUEUED = 0
    STARTED = 1
    FINISHED = 2

class VideoModel(models.Model):

    title = models.CharField(max_length=255, null=False, blank= False)
    title_slug = models.SlugField(null=False, blank= True)
    description = models.TextField(null=True, blank=True)
    video_file_path = models.FileField(
        upload_to=USER_DIRECTORY_PATH,
        validators=[FileExtensionValidator(allowed_extensions=['mp4'])]
    )
    m3u8_file_path = models.CharField(max_length=255, blank=True)
    thumbnail = models.ImageField(
        upload_to=USER_DIRECTORY_PATH,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
    category = models.ForeignKey(CategoryModel, on_delete=models.SET_NULL, null=True)
    genre_type = models.ForeignKey(GenereModel, on_delete=models.SET_NULL, null=True)
    released_date = models.DateField(null= True, blank=True)
    uploaded_date = models.DateTimeField(auto_now_add=True, editable=False)
    processing_status = models.IntegerField(choices=Status.choices, default= Status.QUEUED)
    processing_completed = models.DurationField(null= True, blank=True)
    duration = models.DurationField(null= True, blank=True)
    file_size = models.CharField(max_length=15, null= True, blank= True)
    dimension = models.CharField(max_length=15, null= True, blank= True)
    display_aspect_ratio = models.CharField(max_length=10, null= True, blank= True)
    overall_bit_rate = models.CharField(max_length=15, null= True, blank= True)
    video_bitrate = models.CharField(max_length=15, null= True, blank= True)
    audio_bitrate = models.CharField(max_length=15, null= True, blank= True)

    objects = GetOrNoneManager()

    def save(self, *args, **kwargs):
        if not self.id:
            self.title_slug = slugify(self.title)
            self.processing_status = Status.STARTED
        super(VideoModel, self).save(*args, **kwargs)
    
    def __str__(self):
        return '{} - {}'.format(self.title, self.category)