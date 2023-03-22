import logging
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.versioning import NamespaceVersioning


logger = logging.getLogger('test_series_api')

class VersioningConfig(NamespaceVersioning):
    default_version = 'v1'
    allowed_versions = ['v1','v2']
    version_param = 'version'


class TeaPotApi(APIView):
    permission_classes = (AllowAny,)
    versioning_class = VersioningConfig

    def get(self, request):
        if request.version == 'v1':
            logger.info('Im Tea pot')
            return Response({
                'Message' : "I'm a teapot just kidding your api is working - v1"
            }, status = status.HTTP_200_OK)

        elif request.version == 'v2':
            return Response({
                'Message' : "v2 already damnnn!"
            }, status = status.HTTP_200_OK)