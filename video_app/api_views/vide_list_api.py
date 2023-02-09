from glob import escape
import logging
import traceback

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.versioning import NamespaceVersioning

from media_stream.common import message
from media_stream.utils import custom_exceptions as ce 
from media_stream.utils.custom_pagination import CustomPagination
from media_stream.utils.standard_response import get_response_structure

from ..models import VideoModel, Status
from ..serializers import VideoSerializer

logger = logging.getLogger('video_app')

class VersioningConfig(NamespaceVersioning):
    default_version = 'v1'
    allowed_versions = ['v1']
    version_param = 'version'

class VideoListApi(APIView):
    permission_classes = (AllowAny,)
    versioning_class = VersioningConfig
    page_size = 12

    def get(self, request):
        try :
            if request.version == 'v1':
                search_title= request.GET.get("search-title", None)
                if search_title:
                    videos = VideoModel.filter_cache(
                        title__icontains= search_title,
                        processing_status= Status.FINISHED
                    )
                else:
                    videos = VideoModel.cache_all()
                
                paginator = CustomPagination()
                paginator.page_size = VideoListApi.page_size
                result_page = paginator.paginate_queryset(
                    videos, request
                )
                serializer = VideoSerializer(
                    result_page, many=True, context={'request': request}
                )
                return paginator.get_paginated_response(serializer.data)

        except :
            logger.error(traceback.format_exc())
            raise ce.InternalServerError
        