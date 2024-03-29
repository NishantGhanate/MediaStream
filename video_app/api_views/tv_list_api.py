import logging
import traceback

from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.filters import OrderingFilter
from rest_framework.versioning import NamespaceVersioning
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from media_stream.utils import custom_exceptions as ce 
from media_stream.utils.custom_pagination import CustomPagination

# from ..models import TvChannelModel
# from ..serializers import TvSerializer

logger = logging.getLogger('video_app')

class VersioningConfig(NamespaceVersioning):
    default_version = 'v1'
    allowed_versions = ['v1']
    version_param = 'version'

# class TvListApi(generics.ListAPIView):
#     permission_classes = (AllowAny,)
#     versioning_class = VersioningConfig
#     serializer_class = TvSerializer
#     pagination_class = CustomPagination
#     filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
#     filterset_fields = (
#         'channel_name_slug', 'language__name_slug', 
#         'category__name_slug'
#     )
#     search_fields = ('channel_name', )
#     ordering = ('-id', )
#     queryset = TvChannelModel.cache_all()
    
#     def get(self, request, *args, **kwargs):
#         try :
#             if request.version == 'v1':
#                 return self.list(request, *args, **kwargs)
#         except :
#             logger.error(traceback.format_exc())
#             raise ce.InternalServerError
        