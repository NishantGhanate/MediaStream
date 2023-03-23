from django.conf import settings

def get_google_form(request):
    return {
        'get_google_form' :  settings.GOOGLE_FORM_URL
    }

def get_whatsapp_link(request):
    return {
        'get_whatsapp_link': settings.WHATS_APP_LINK
    }