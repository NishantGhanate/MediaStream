
def get_response_structure(
    status_code= None, success= False, message= None, data= None
    ):
    result =  {
        'status_code' : status_code,
        'success' : success,
        'message' : message,
        'data' : data
    }
    return result