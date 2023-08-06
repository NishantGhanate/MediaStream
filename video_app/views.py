import pdb
import logging
import traceback
from django.views import View
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.db.models import Q

from video_app.forms import ContactUsForm
from video_app.models import TvChannelModel, VideoProcessingStatus, VideoModel

va_logger = logging.getLogger('video_app')

class HomeView(View):
    template_name = 'home.html'
    
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context= context)

class ContactUsView(View):
    template_name = 'contact.html'
    
    def get(self, request, *args, **kwargs):
        form = ContactUsForm(None)
        context = {
            'form' : form
        }
        return render(request, self.template_name, context= context)

    def post(self, request, *args, **kwargs):
        contact_us = ContactUsForm(request.POST)
        context = {}
        if contact_us.is_valid():
            context['form'] = ContactUsForm(None)
            context['success'] = True
            context['message'] = 'Thank you contacting us'
            contact_us.save()
        else:
            context['form'] = contact_us
        return render(request, self.template_name, context= context)



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

class VideoListView(View):
    template_name = 'videos/main.html'
    page_size = 12

    def get(self, request, *args, **kwargs):
        context = {}
        
        search_title = request.GET.get("search-title")
        if search_title:
            videos = VideoModel.filter_cache(
                title__icontains= search_title,
                processing_status= VideoProcessingStatus.FINISHED
            )
        else:
            videos = VideoModel.filter_cache(processing_status= VideoProcessingStatus.FINISHED)
        
        paginator = Paginator(videos, VideoListView.page_size)
        page = request.GET.get('page', 1)
        try:
            videos = paginator.page(page)
        except PageNotAnInteger:
            videos = paginator.page(1)
        except EmptyPage:
            videos = paginator.page(paginator.num_pages)

        
        if len(videos):
            context['videos'] = videos
        elif search_title:
            context['message'] = f'Sorry could not find {search_title}'
        return render(request, self.template_name, context= context)

class VideoDetailViiew(View):
    template_name = 'videos/watch_video.html'

    def get(self, request, *args, **kwargs):
        video = None
        try:
            video = VideoModel.filter_cache(
                title_slug = kwargs['video_title'],
                processing_status= VideoProcessingStatus.FINISHED
            ).first()
            
        except :
            va_logger.error(traceback.format_exc())
            return render(request, self.template_name, context= {
                'message' : 'Ops something went wrong !'
            })
        
        return render(request, self.template_name, context= {
            'video' : video
        })

class VideoCaterogry(View):
    template_name = 'videos/main.html'
    page_size = 12

    def get(self, request, *args, **kwargs):
        context = {}
        search_title = request.GET.get("search-title")
        
        # TODO : validate category slug
        if search_title:
            videos = VideoModel.filter_cache(
                title__icontains= search_title,
                category__name_slug = kwargs['video_category'],
                processing_status= VideoProcessingStatus.FINISHED
            )
        else:

            videos = VideoModel.filter_cache(
                category__name_slug = kwargs['video_category'],
                processing_status= VideoProcessingStatus.FINISHED
            )
        
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
            context['message'] = f'Sorry could not find {search_title}'
        return render(request, self.template_name, context= context)
