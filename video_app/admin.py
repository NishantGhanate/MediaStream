from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from video_app.models import CustomUser, CategoryModel, VideoModel
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
        'video_title_slug', 'video_file_m3u8', 
        'video_error_msg', 'video_processing_status'
    )
    form = VideoForm

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(CategoryModel)
admin.site.register(VideoModel, VideoAdmin)