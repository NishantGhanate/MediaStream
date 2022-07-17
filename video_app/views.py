import logging
import traceback
from django.views import View
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from video_app.models import VideoModel

va_logger = logging.getLogger('video_app')

class HomeView(View):
    template_name = 'videos/videos_page.html'

    def get(self, request, *args, **kwargs):
        context = {}
        videos = VideoModel.objects.all()
        paginator = Paginator(videos, 10)
        page = request.GET.get('page', 1)
        try:
            videos = paginator.page(page)
        except PageNotAnInteger:
            videos = paginator.page(1)
        except EmptyPage:
            videos = paginator.page(paginator.num_pages)

        context['videos'] = videos
        return render(request, self.template_name, context= context)

    def post(self, request, *args, **kwargs):
        # form = self.form_class(request.POST)
        # if form.is_valid():
        #     # <process form cleaned data>
        #     return HttpResponseRedirect('/success/')

        return render(request, self.template_name, context = {})

class WatchVideoView(View):
    template_name = 'videos/watch.html'

    def get(self, request, *args, **kwargs):
        video = None
        try:
            video = VideoModel.objects.get(title_slug = kwargs['video_title'])
        except :
            va_logger.error(traceback.format_exc())
            # TODO : redirect to home page
        
        return render(request, self.template_name, context= {
            'video' : video
        })
    