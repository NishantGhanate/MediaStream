from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from captcha.fields import CaptchaField, CaptchaTextInput

from video_app import models

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = models.CustomUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = models.CustomUser
        fields = ('email',)

class LanguageForm(forms.ModelForm):
    
    class Meta: 
        model = models.LanguageModel
        fields = '__all__'

class VideoForm(forms.ModelForm):
    
    # validators=[validate_even]

    class Meta: 
        model = models.VideoModel
        fields = '__all__'
        widgets = {
            'video_file_path': forms.FileInput(attrs={'accept':'.mp4'})
        }

class ContactUsForm(forms.ModelForm):
    full_name = forms.CharField(label='Full name', max_length=50,
            widget=forms.TextInput(attrs={'placeholder': 'Full Name'})
        )
    mobile_no = forms.CharField(label='Mobile No', max_length=15,
            widget=forms.TextInput(attrs={'placeholder': 'Mobile No'})
        )
    email = forms.EmailField(label='Email-address', max_length=75,
            widget=forms.TextInput(attrs={'placeholder': 'E-mail address'})
        )
    message = forms.CharField(max_length=500, widget=forms.Textarea(
            attrs={'placeholder': 'Your message'})
        )
    captcha = CaptchaField(label='Please enter the characters in the image',
            widget=CaptchaTextInput(attrs={'placeholder': 'CAPTCHA !'})
        )

    class Meta: 
        model = models.ContactUsModel
        fields = '__all__'

class CategoryForm(forms.ModelForm):
    class Meta: 
        model = models.CategoryModel
        fields = '__all__'

class GenreForm(forms.ModelForm):
    class Meta: 
        model = models.GenreModel
        fields = '__all__'