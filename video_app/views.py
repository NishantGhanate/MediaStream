import logging
from django.views import View
from django.shortcuts import render
from django.http import HttpResponseRedirect
from video_app.models import VideoModel

logger = logging.getLogger('video_app')

class HomeView(View):
    template_name = 'videos/videos_page.html'

    def get(self, request, *args, **kwargs):
        videos = VideoModel.objects.all()
        return render(request, self.template_name, context= {
            'videos' : videos
        })

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
            video = VideoModel.objects.get(video_title_slug = kwargs['video_title'])
        except :
            pass
        
        return render(request, self.template_name, context= {
            'video' : video
        })
    