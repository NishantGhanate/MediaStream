from django.conf import settings

def get_google_form(request):
    return {
        'get_google_form' :  settings.GOOGLE_FORM_URL
    }
    