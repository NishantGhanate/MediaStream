from django.urls import path
from . import views

urlpatterns = [
    path(
        '', 
        views.HomeView.as_view(),
        name='home-view'
    ),
    path(
        'watch/<slug:video_title>',
        views.WatchVideoView.as_view(), 
        name='watch-video-view'
    ),
]