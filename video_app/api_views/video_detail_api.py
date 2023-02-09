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

class VideoDetailApi(APIView):
    permission_classes = (AllowAny,)
    versioning_class = VersioningConfig
    page_size = 12

    def get(self, request, **kwargs):
        try :
            if request.version == 'v1':
                video = VideoModel.filter_cache(
                    title_slug = kwargs['video_title'],
                    processing_status= Status.FINISHED
                ).first()
                    
                if video is None:
                    raise ce.ResourceNotFound

                video = VideoSerializer(
                    instance= video, many= False
                ).data

                response = get_response_structure(
                    status_code= status.HTTP_200_OK,
                    success= True,
                    message= message.DATA_FETHCED_SUCCESSFULLY,
                    data= video
                )             
                return Response(response, status = response['status_code'])

        except ce.ResourceNotFound as _:
            raise ce.ResourceNotFound

        except :
            logger.error(traceback.format_exc())
            raise ce.InternalServerError
        