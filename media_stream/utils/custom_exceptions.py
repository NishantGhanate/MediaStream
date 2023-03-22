from rest_framework import status
from rest_framework.exceptions import APIException
from ..common import message

class VideoProcessFailed(Exception):
    """Exception raised for errors in the input salary.

    Attributes:
        salary -- input salary which caused the error
        message -- explanation of the error
    """

    def __init__(self, file_name, message="Failed to process file"):
        self.file_name = file_name
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f'{self.file_name} -> {self.message}'

class InternalServerError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = message.INTERNAL_SERVER_ERROR
    default_code = 'internal_server_error'


class VersionNotSupported(APIException):
    status_code = status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED
    default_detail = message.VERSION_NOT_SUPPORTED
    default_code = 'version_not_supported'

class ResourceNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = message.RESOURCE_NOT_FOUND
    default_code = 'resouce_not_found'
