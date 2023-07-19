import pdb
import logging
import traceback
from django.http import Http404

from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.versioning import NamespaceVersioning
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_list_or_404, get_object_or_404

from media_stream.utils import custom_exceptions as ce 
from media_stream.utils.custom_pagination import CustomPagination

from ..models import VideoModel, VideoProcessingStatus
from ..serializers import VideoSerializer
from ..filters import VideoModelFilter

logger = logging.getLogger('video_app')

class VersioningConfig(NamespaceVersioning):
    default_version = 'v1'
    allowed_versions = ['v1']
    version_param = 'version'


class MultipleFieldLookupMixin(object):

    def get_object(self):
        # pdb.set_trace()
        queryset = self.get_queryset()             
        queryset = self.filter_queryset(queryset)  
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs.get(field, None):  
                filter[field] = self.kwargs[field]
        obj = get_list_or_404(queryset, **filter)  # Lookup the object
        
        return obj

class VideoCategoryApi(generics.ListAPIView):
    permission_classes = (AllowAny,)
    versioning_class = VersioningConfig
    serializer_class = VideoSerializer
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('title', )
    ordering = ('-id', )
    lookup_field = 'category__name_slug'
    queryset = VideoModel.filter_cache(
        processing_status= VideoProcessingStatus.FINISHED
    )

    def get_queryset(self):
        qs = super(VideoCategoryApi, self).get_queryset()
        filter = {}

        if self.kwargs.get(self.lookup_field, None):  
            filter[self.lookup_field] = self.kwargs[self.lookup_field]

        qs = qs.filter(**filter)
        if not qs:
            raise ce.ResourceNotFound(
                detail= f"No {qs.model._meta.object_name} matches the given query." 
            )
        return qs

    def get(self, request, *args, **kwargs):
        try :
            if request.version == 'v1':
                return self.list(request, *args, **kwargs)
        except ce.ResourceNotFound as rnf:
            logger.error(rnf.detail)
            raise ce.ResourceNotFound(detail= rnf.detail)
        except :
            logger.error(traceback.format_exc())
            raise ce.InternalServerError