from rest_framework import serializers
from . import models

class LanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.LanguageModel
        fields = '__all__'
        
class TvSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TvChannelModel
        fields = '__all__'

class GenereSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.GenreModel
        fields = '__all__'
    
    def to_representation(self, obj):
        return  {
            'name' : obj.name,
            'slug' : obj.name_slug
        }

class VideoSerializer(serializers.ModelSerializer):

    language = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    genre = GenereSerializer(read_only=True, many=True)
    m3u8_file_path = serializers.SerializerMethodField()

    class Meta:
        model = models.VideoModel
        exclude = (
            'processing_status', 'processing_completed', 'video_file_path',
            'uploaded_date', 
        )
        depth = 1
        
        
    def get_m3u8_file_path(self, obj):
        host = self.context.get("request").build_absolute_uri('/media')
        return f"{host}{obj.m3u8_file_path}"

    def get_language(self, obj):
        return {
            'name' : obj.language.name,
            'slug' : obj.language.name_slug
        }

    def get_category(self, obj):
        return {
            'name' : obj.category.name,
            'slug' : obj.category.name_slug
        }
    
        
       

        