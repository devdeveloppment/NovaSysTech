from django.shortcuts import render
from .models import FAQ

def faq(request):
    faqs = FAQ.objects.filter(est_actif=True)
    ctx = {
        'page': 'faq',
        'faqs_general': faqs.filter(categorie='general'),
        'faqs_services': faqs.filter(categorie='services'),
        'faqs_devis': faqs.filter(categorie='devis'),
    }
    return render(request, 'faq/faq.html', ctx)
