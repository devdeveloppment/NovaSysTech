from django.conf import settings

def global_context(request):
    return {
        'PHONE_1': getattr(settings, 'PHONE_1', '+228 79 92 81 81'),
        'PHONE_2': getattr(settings, 'PHONE_2', '+228 70 30 79 68'),
        'EMAIL_CONTACT': getattr(settings, 'EMAIL_CONTACT', 'contact@novasystechn.com'),
        'EMAIL_SUPPORT': getattr(settings, 'EMAIL_SUPPORT', 'contact@novasystechn.com'),
        'WHATSAPP_NUMBER': getattr(settings, 'WHATSAPP_NUMBER', '22879928181'),
        'ADRESSE': getattr(settings, 'ADRESSE', 'Agoè Assiyéyé, derrière Station Cap Togo, Lomé, Togo'),
        'MAPS_URL': getattr(settings, 'MAPS_URL', ''),
        'RECAPTCHA_PUBLIC_KEY': getattr(settings, 'RECAPTCHA_PUBLIC_KEY', ''),
        'SITE_URL': getattr(settings, 'SITE_URL', ''),
    }
