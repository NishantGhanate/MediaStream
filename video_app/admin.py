from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django_celery_results.admin import TaskResultAdmin
from django_celery_results.models import TaskResult

from video_app.models import (
    CustomUser, LanguageModel, CategoryModel, GenreModel,
    VideoModel, TvChannelModel
)
from video_app.forms import (
    CustomUserCreationForm, CustomUserChangeForm, LanguageForm,
    VideoForm
)
from .admin_actions import retry_celery_task_admin_action

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
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
    form = LanguageForm

class VideoAdmin(admin.ModelAdmin):
    readonly_fields = (
        'title_slug', 'm3u8_file_path', 'processing_completed',
        'processing_status', 'file_size', 'dimension',
        'duration', 'display_aspect_ratio', 'overall_bit_rate',
        'video_bitrate', 'audio_bitrate'
        
    )
    form = VideoForm

class CustomTaskResultAdmin(TaskResultAdmin):
    actions = [retry_celery_task_admin_action, ]


admin.site.unregister(TaskResult)
admin.site.register(TaskResult, CustomTaskResultAdmin)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(LanguageModel, LanguageAdmin)
admin.site.register(CategoryModel)
admin.site.register(GenreModel)
admin.site.register(VideoModel, VideoAdmin)
admin.site.register(TvChannelModel)