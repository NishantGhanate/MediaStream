from django.urls import path
from . import views

urlpatterns = [
    path(
        '', 
        views.HomeView.as_view(),
        name='home-view'
    ),
    path(
        'contact-us', 
        views.ContactUsView.as_view(),
        name='contact-us'
    ),
    path(
        'video', 
        views.VideoListView.as_view(),
        name='video-list-view'
    ),
    path(
        'video/watch/<slug:video_title>',
        views.VideoDetailViiew.as_view(), 
        name='video-detail-view'
    ),
    path(
        'video/<slug:video_category>/',
        views.VideoCaterogry.as_view(), 
        name='video-category-view'
    ),
    path(
        'tv', 
        views.TvListView.as_view(),
        name='tv-list-view'
    ),
    path(
        'tv/<slug:channel_name_slug>', 
        views.TvDetailView.as_view(),
        name='tv-detail-view'
    )
]
