import logging
import traceback
from django.views import View
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.db.models import Q
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from video_app.models import VideoModel

va_logger = logging.getLogger('video_app')

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

class HomeView(View):
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
            videos = VideoModel.cache_all()
        
        paginator = Paginator(videos, HomeView.page_size)
        page = request.GET.get('page', 1)
        try:
            videos = paginator.page(page)
        except PageNotAnInteger:
            videos = paginator.page(1)
        except EmptyPage:
            videos = paginator.page(paginator.num_pages)

        context['videos'] = videos
        return render(request, self.template_name, context= context)

class WatchVideoView(View):
    template_name = 'videos/watch.html'

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
    