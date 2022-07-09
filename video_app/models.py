import logging
import traceback

from os import sep as os_slash
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from django.utils import timezone
from django.utils.text import slugify


from video_app.managers import CustomUserManager, GetOrNoneManager

logger = logging.getLogger('video_app')

def USER_DIRECTORY_PATH(instance, file_name):
    try:
        return os_slash.join([
            instance.video_category.category_name,
            instance.video_category.category_lang,
            instance.video_title_slug,
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
    category_name = models.CharField(max_length= 50, null=False, blank=False)
    category_lang = models.CharField(max_length= 50, null=False, blank=False)
    objects = GetOrNoneManager()

    class Meta:
        unique_together = ('category_name', 'category_lang',)

    def __str__(self):
        return '{} - {}'.format(self.category_lang, self.category_name)
        
class Status(models.IntegerChoices):
    FAILED = -1
    QUEUED = 0
    STARTED = 1
    FINISHED = 2


class VideoModel(models.Model):

    video_title = models.CharField(max_length=255, null=False, blank= False)
    video_title_slug = models.SlugField(null=False, blank= True)
    video_description = models.TextField(null=True, blank=True)
    video_file_name = models.FileField(upload_to=USER_DIRECTORY_PATH)
    video_file_m3u8 = models.CharField(max_length=255, blank=True)
    video_thumbnail = models.ImageField(upload_to=USER_DIRECTORY_PATH)
    video_category = models.ForeignKey(CategoryModel, on_delete=models.SET_NULL, null=True)
    video_released_date = models.DateField()
    video_uploaded_date = models.DateTimeField(auto_now_add=True, editable=False)
    video_processing_status = models.IntegerField(choices=Status.choices, default= Status.QUEUED)
    video_error_msg = models.TextField(null=True, blank=True)
    video_processing_completed = models.DateTimeField(null= True, blank=True)

    objects = GetOrNoneManager()

    def save(self, *args, **kwargs):
        if not self.id:
            self.video_title_slug = slugify(self.video_title)
            self.video_processing_status = Status.STARTED
        super(VideoModel, self).save(*args, **kwargs)
    
    def __str__(self):
        return '{} - {}'.format(self.video_title, self.video_category)