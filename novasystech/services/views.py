from django.shortcuts import render, get_object_or_404
from .models import Service

FORMATIONS = [
    {
        'titre': 'Formation Cybersécurité',
        'image': '/static/images/formation-cybersecurite.jpg',
        'modules': ['Base de la cybersécurité', 'Sécurité des postes de travail', 'Sécurité du réseau', 'Détection des incidents', 'Test d\'intrusion (Pentest)'],
        'debut': '20 Nov 2025', 'duree': '4 Semaines',
        'inscription': '5 000 FCFA', 'tarif': '50 000 FCFA',
    },
    {
        'titre': 'Formation Déploiement Wi-Fi MikroTik',
        'image': '/static/images/formation-mikrotik.jpg',
        'modules': ['Normes et équipements MikroTik', 'Configurations de base', 'Création réseau Wi-Fi sécurisé', 'Portail captif', 'Gestion des utilisateurs', 'Contrôle bande passante'],
        'debut': '20 Nov 2025', 'duree': '4 Semaines',
        'inscription': '5 000 FCFA', 'tarif': '50 000 FCFA',
    },
    {
        'titre': 'Formation Maintenance Informatique',
        'image': '/static/images/formation-maintenance.jpg',
        'modules': ['Assemblage & démontage PC', 'Détection & réparation de pannes', 'Remplacement des pièces', 'Installation OS', 'Formatage & sauvegarde', 'Diagnostic matériel'],
        'debut': '20 Nov 2025', 'duree': '4 Semaines',
        'inscription': '5 000 FCFA', 'tarif': '50 000 FCFA',
    },
    {
        'titre': 'Formation Caméras de Surveillance',
        'image': '/static/images/formation-cctv.jpg',
        'modules': ['Types de caméras', 'Installation & câblage', 'Configuration DVR/NVR', 'Connexion à distance', 'Sauvegarde & stockage', 'Sécurité réseau CCTV'],
        'debut': '20 Nov 2025', 'duree': '4 Semaines',
        'inscription': '5 000 FCFA', 'tarif': '50 000 FCFA',
    },
]

def services_hub(request):
    services = Service.objects.filter(est_actif=True).order_by('ordre')
    ctx = {'services': services, 'page': 'services'}
    return render(request, 'services/hub.html', ctx)

def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, est_actif=True)
    autres = Service.objects.filter(est_actif=True).exclude(pk=service.pk).order_by('ordre')[:5]
    ctx = {
        'service': service,
        'autres': autres,
        'page': 'services',
        'formations': FORMATIONS if slug == 'formation-certification' else [],
    }
    return render(request, 'services/detail.html', ctx)
