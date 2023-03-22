from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from ..common import message
from .standard_response import get_response_structure


class CustomPagination(PageNumberPagination):

    def get_paginated_response(self, data):
        response_struct = get_response_structure(
            status_code = status.HTTP_200_OK,
            success= True, 
            message = message.DATA_FETHCED_SUCCESSFULLY
        )
        response_struct['data'] = {
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        }
        return Response(response_struct, status=response_struct['status_code'])
