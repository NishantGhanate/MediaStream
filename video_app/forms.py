from django.forms import ModelForm, FileInput
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from video_app.models import CustomUser, VideoModel


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)


class VideoForm(ModelForm):
    
    # validators=[validate_even]

    class Meta: 
        model = VideoModel
        fields = '__all__'
        # widgets = {
        #     'video_file_path': FileInput(attrs={'accept':'.mp4'})
        # }