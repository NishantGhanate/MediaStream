from . import models
from django_filters import CharFilter, FilterSet

import logging

logger = logging.getLogger('video_app')

class VideoModelFilter(FilterSet):

    # genre = CharFilter(method = 'get_genre')
    # language = CharFilter(method = 'get_language', field_name='language__slug_name')
    # category = CharFilter(method = 'get_category', field_name='category__slug_name')

    class Meta:
        model = models.VideoModel
        fields = ('genre',)
    
    # def get_genre(self, queryset, field_name, value):
    #     logger.info(queryset, field_name, value)
    #     return queryset.filter(genre__name_slug = value)

    # def get_language(self, queryset, field_name, value):
    #     return queryset.filter(language__name_slug = value)
    
    # def get_category(self, queryset, field_name, value):
    #     return queryset.filter(category__name_slug = value)