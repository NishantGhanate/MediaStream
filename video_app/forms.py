from django.forms import ModelForm
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
    
    class Meta: 
        model = VideoModel
        fields = '__all__'
        