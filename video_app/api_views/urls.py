from django.urls import path

from .teapot import TeaPotApi
from .tv_list_api import TvListApi
from .tv_detail_api import TvDetailApi
from .vide_list_api import VideoListApi
from .video_detail_api import VideoDetailApi
from .video_caterogry_api import VideoCategoryApi

urlpatterns = [
    path('tea-apot-api', 
        TeaPotApi.as_view(),
        name='teapot-api-api'
    ),
    path(
        'tv', 
        TvListApi.as_view(),
        name='tv-list-api'
    ),
    path(
        'tv/<slug:channel_name_slug>', 
        TvDetailApi.as_view(),
        name='tv-detail-api'
    ),
    path(
        'video', 
        VideoListApi.as_view(),
        name='video-list-api'
    ),
    path(
        'video/watch/<slug:video_title>',
        VideoDetailApi.as_view(), 
        name='video-detail-api'
    ),
    path(
        'video/<slug:video_category>/',
        VideoCategoryApi.as_view(), 
        name='video-category-api'
    )
]
