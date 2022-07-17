from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from video_app.models import (
    CustomUser, CategoryModel,
    GenereModel, VideoModel
)
from video_app.forms import (
    CustomUserCreationForm, CustomUserChangeForm, VideoForm
)
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

class VideoAdmin(admin.ModelAdmin):
    readonly_fields = (
        'title_slug', 'm3u8_file_path', 'processing_completed',
        'processing_status', 'file_size', 'dimension',
        'duration', 'display_aspect_ratio', 'overall_bit_rate',
        'video_bitrate', 'audio_bitrate'
        
    )
    form = VideoForm

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(GenereModel)
admin.site.register(CategoryModel)
admin.site.register(VideoModel, VideoAdmin)