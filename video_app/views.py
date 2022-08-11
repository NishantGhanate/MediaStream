import logging
import traceback
from django.views import View
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.db.models import Q

from video_app.models import Status, VideoModel, TvChannelModel

va_logger = logging.getLogger('video_app')

class HomeView(View):
    template_name = 'home.html'
    
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context= context)
    
class VideoListView(View):
    template_name = 'videos/main.html'
    page_size = 12

    def get(self, request, *args, **kwargs):
        context = {}
        
        search_title = request.GET.get("search-title")
        if search_title:
            videos = VideoModel.filter_cache(
                title__icontains= search_title
            )
        else:
            videos = VideoModel.filter_cache(processing_status= Status.FINISHED)
        
        paginator = Paginator(videos, VideoListView.page_size)
        page = request.GET.get('page', 1)
        try:
            videos = paginator.page(page)
        except PageNotAnInteger:
            videos = paginator.page(1)
        except EmptyPage:
            videos = paginator.page(paginator.num_pages)

        if videos:
            context['videos'] = videos
        elif search_title:
            context['error_message'] = f'Sorry could not find {search_title}'
        return render(request, self.template_name, context= context)

class VideoDetailViiew(View):
    template_name = 'videos/watch_video.html'

    def get(self, request, *args, **kwargs):
        video = None
        try:
            video = VideoModel.filter_cache(
                title_slug = kwargs['video_title']
                ).first()
            
        except :
            va_logger.error(traceback.format_exc())
            # TODO : renders ops page
        
        return render(request, self.template_name, context= {
            'video' : video
        })

class TvListView(View):
    template_name = 'tv/main.html'
    page_size = 12

    def get(self, request, *args, **kwargs):
        context = {}
        
        search_channel= request.GET.get("search-channel")
        if search_channel:
            channels = TvChannelModel.filter_cache(
                channel_name__icontains= search_channel
            )
        else:
            channels = TvChannelModel.cache_all()
        
        paginator = Paginator(channels, TvListView.page_size)
        page = request.GET.get('page', 1)
        try:
            channels = paginator.page(page)
        except PageNotAnInteger:
            channels = paginator.page(1)
        except EmptyPage:
            channels = paginator.page(paginator.num_pages)

        if channels:
            context['channels'] = channels
        elif search_channel:
            context['error_message'] = f'Sorry could not find {search_channel}'
        return render(request, self.template_name, context= context)

class TvDetailView(View):
    template_name = 'tv/watch_channel.html'

    def get(self, request, *args, **kwargs):
        channel = None
        try:
            channel = TvChannelModel.filter_cache(
                channel_name_slug = kwargs['channel_name_slug']
                ).first()
            
        except :
            va_logger.error(traceback.format_exc())
            # TODO : renders ops page
        
        return render(request, self.template_name, context= {
            'channel' : channel
        })