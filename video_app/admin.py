from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django_celery_results.admin import TaskResultAdmin
from django_celery_results.models import TaskResult

from video_app import models
from video_app import forms

from .admin_actions import retry_celery_task_admin_action

class CustomUserAdmin(UserAdmin):
    add_form = forms.CustomUserCreationForm
    form = forms.CustomUserChangeForm
    model = models.CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'password1', 'password2', 
                'is_staff', 'is_active'
            )}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

class LanguageAdmin(admin.ModelAdmin):
    readonly_fields = ('name_slug',)
    form = forms.LanguageForm


class GenreAdmin(admin.ModelAdmin):
    readonly_fields = ('name_slug',)
    form = forms.GenreForm

class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('name_slug',)
    form = forms.CategoryForm


class VideoAdmin(admin.ModelAdmin):
    readonly_fields = (
        'title_slug', 'm3u8_file_path', 'processing_completed',
        'processing_status', 'file_size', 'dimension',
        'duration', 'display_aspect_ratio', 'overall_bit_rate',
        'video_bitrate', 'audio_bitrate'
        
    )
    form = forms.VideoForm

class CustomTaskResultAdmin(TaskResultAdmin):
    actions = [retry_celery_task_admin_action, ]


admin.site.unregister(TaskResult)
admin.site.register(TaskResult, CustomTaskResultAdmin)

admin.site.register(models.CustomUser, CustomUserAdmin)
admin.site.register(models.ContactUsModel)
admin.site.register(models.LanguageModel, LanguageAdmin)
admin.site.register(models.GenreModel, GenreAdmin)
admin.site.register(models.CategoryModel, CategoryAdmin)
admin.site.register(models.TvChannelModel)
admin.site.register(models.VideoModel, VideoAdmin)