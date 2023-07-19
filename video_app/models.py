import logging
import traceback

from os import sep as os_slash
from unicodedata import category
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from django.utils import timezone
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator

from video_app.mixins import ModelCacheMixin
from video_app.managers import CustomUserManager, GetOrNoneManager

logger = logging.getLogger('video_app')
# validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
# 

def USER_DIRECTORY_PATH(instance, file_name):
    try:
        if instance.category and instance.language:
            storage_path = [
                instance.category.name,
                instance.language.name,
                instance.title_slug,
                file_name
            ]
        else:
            storage_path = [instance.__name__, file_name]

        return os_slash.join(storage_path)
    except :
        logger.error(traceback.format_exc())

def STORE_TV_THUMBNAIL(instance, file_name):
    print(instance.__dict__)
    print(instance._meta.model_name)
    storage_path = [instance._meta.model_name, file_name]

    return os_slash.join(storage_path)

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

class LanguageModel(models.Model):
    name = models.CharField(max_length= 50, null=False, blank=False, unique= True)
    name_slug = models.SlugField(blank=True)
    objects = GetOrNoneManager()

    class Meta:
        ordering = ['-id']

    def save(self, *args, **kwargs):
        if not self.id:
            self.name_slug = slugify(self.name)
        super(LanguageModel, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'

class GenreModel(models.Model):
    name = models.CharField(max_length= 50, null=False, blank=False)
    name_slug = models.SlugField(blank=True)
    objects = GetOrNoneManager()

    class Meta:
        ordering = ['-id']

    def save(self, *args, **kwargs):
        if not self.id:
            self.name_slug = slugify(self.name)
        super(GenreModel, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'

class CategoryModel(models.Model):
    name = models.CharField(max_length= 100)
    name_slug = models.SlugField(blank=True)
    
    class Meta:
        ordering = ['-id']

    def save(self, *args, **kwargs):
        if not self.id:
            self.name_slug = slugify(self.name)
        super(CategoryModel, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'

class VideoProcessingStatus(models.IntegerChoices):
    FAILED = -1
    QUEUED = 0
    STARTED = 1
    FINISHED = 2

class VideoModel(models.Model, ModelCacheMixin):
    CACHE_KEY = "VideoModel"
    CACHED_RELATED_OBJECT = ["language", "category"]
    CACHED_PREFETCH_OBJECT = ["genre"]

    title = models.CharField(max_length=255, blank= False)
    title_slug = models.SlugField(blank= True)
    description = models.TextField(null=True, blank=True)
    video_file_path = models.FileField(upload_to=USER_DIRECTORY_PATH)
    m3u8_file_path = models.CharField(max_length=255, blank=True)
    thumbnail = models.ImageField(upload_to=USER_DIRECTORY_PATH)
    language = models.ForeignKey(LanguageModel, on_delete=models.SET_NULL, null=True)
    genre = models.ManyToManyField(GenreModel)
    category = models.ForeignKey(CategoryModel, on_delete=models.SET_NULL, null=True)
    released_date = models.DateField(null= True, blank=True)
    uploaded_date = models.DateTimeField(auto_now_add=True, editable=False)
    processing_status = models.IntegerField(choices=VideoProcessingStatus.choices, default= VideoProcessingStatus.QUEUED)
    processing_completed = models.DurationField(null= True, blank=True)
    duration = models.DurationField(null= True, blank=True)
    file_size = models.CharField(max_length=15, null= True, blank= True)
    dimension = models.CharField(max_length=15, null= True, blank= True)
    display_aspect_ratio = models.CharField(max_length=10, null= True, blank= True)
    overall_bit_rate = models.CharField(max_length=15, null= True, blank= True)
    video_bitrate = models.CharField(max_length=15, null= True, blank= True)
    audio_bitrate = models.CharField(max_length=15, null= True, blank= True)

    objects = GetOrNoneManager()

    class Meta:
        ordering = ['-id']
        
    def save(self, *args, **kwargs):
        if not self.id:
            self.title_slug = slugify(self.title)
            self.processing_status = VideoProcessingStatus.STARTED
        super(VideoModel, self).save(*args, **kwargs)
    
    def __str__(self):
        return '{} - {}'.format(self.title, self.category)

class TvChannelModel(models.Model, ModelCacheMixin):
    CACHE_KEY = "TvChannel"
    CACHED_RELATED_OBJECT = ["language", "category"]
    CACHED_PREFETCH_OBJECT = None

    channel_name = models.CharField(max_length=255, blank= False)
    channel_name_slug = models.SlugField(blank= True)
    description = models.TextField(null=True, blank=True)
    m3u8_url = models.URLField()
    thumbnail = models.ImageField(upload_to=STORE_TV_THUMBNAIL)
    language = models.ForeignKey(LanguageModel, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(CategoryModel, on_delete=models.SET_NULL, null=True)
    objects = GetOrNoneManager()

    class Meta:
        ordering = ['-id']
        unique_together = ['channel_name', 'language']
        
        
    def save(self, *args, **kwargs):
        if not self.id:
            self.channel_name_slug = slugify(self.channel_name)
            
        super(TvChannelModel, self).save(*args, **kwargs)
    
    def __str__(self):
        return '{} - {}'.format(self.channel_name, self.language)

class ContactUsModel(models.Model):
    full_name = models.CharField(max_length= 50)
    mobile_no = models.CharField(max_length= 15)
    email = models.EmailField(max_length= 75)
    message = models.TextField(max_length=500)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return '{} - {}'.format(self.full_name, self.mobile_no)