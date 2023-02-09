from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if 'message' in response.data:
            response.data = {
                'success': False,
                'status_code': response.status_code,
                'message': response.data['message'],
                'data': response.data.get('data', None)
            }
        else:
            new_dict = dict(response.data)
            message = ''
            for key in new_dict:
                message = message.join(new_dict[key])
            response.data = {
                'success' : False,
                'status_code' : response.status_code,
                'message' : message,
                'data': response.data.get('data', None)
            }

    return response