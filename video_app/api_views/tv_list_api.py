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

from ..models import TvChannelModel
from ..serializers import TvSerializer

logger = logging.getLogger('video_app')

class VersioningConfig(NamespaceVersioning):
    default_version = 'v1'
    allowed_versions = ['v1']
    version_param = 'version'

class TvListApi(APIView):
    permission_classes = (AllowAny,)
    versioning_class = VersioningConfig
    page_size = 12

    def get(self, request):
        try :
            if request.version == 'v1':
                search_channel= request.GET.get("search-channel")
                if search_channel:
                    channels = TvChannelModel.filter_cache(
                        channel_name__icontains= search_channel
                    )
                else:
                    channels = TvChannelModel.cache_all()
                
                paginator = CustomPagination()
                paginator.page_size = TvListApi.page_size
                result_page = paginator.paginate_queryset(
                    channels, request
                )
                serializer = TvSerializer(
                    result_page, many=True, context={'request': request}
                )
                return paginator.get_paginated_response(serializer.data)

        except :
            logger.error(traceback.format_exc())
            raise ce.InternalServerError
        