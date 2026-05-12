from django.shortcuts import render
from .models import Projet

DEMO_PROJETS = [
    ('https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=600&q=80', 'Banque Atlantique Togo', 'cctv', 'Déploiement système surveillance IP intelligent HD sur 12 agences nationales.'),
    ('https://images.unsplash.com/photo-1544197150-b99a580bb7a8?w=600&q=80', 'Ecobank Transnational', 'cloud', 'Migration hybride vers Azure et optimisation des infrastructures serveurs.'),
    ('https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600&q=80', 'Port Autonome de Lomé', 'reseaux', 'Refonte complète de infrastructure fibre optique et wifi industriel.'),
    ('https://images.unsplash.com/photo-1591370874773-6702e8f12fd8?w=600&q=80', 'Togo Cellulaire (Togocom)', 'maintenance', 'Contrat maintenance préventive du parc informatique du siège social.'),
    ('https://images.unsplash.com/photo-1497366216548-37526070297c?w=600&q=80', 'Ministère Économie Numérique', 'maintenance', 'Audit de sécurité pour la digitalisation des services publics.'),
    ('https://images.unsplash.com/photo-1562774053-701939374585?w=600&q=80', 'Université de Lomé', 'reseaux', 'Extension backbone réseau pour 20 000 connexions simultanées.'),
]

def portfolio_list(request):
    projets = Projet.objects.filter(est_publie=True)
    cat = request.GET.get('cat', 'tous')
    if cat and cat != 'tous':
        projets = projets.filter(categorie=cat)
    ctx = {
        'projets': projets,
        'cat_active': cat,
        'page': 'portfolio',
        'categories': Projet.CATEGORIES,
        'demo_projets': DEMO_PROJETS if not projets.exists() else [],
    }
    return render(request, 'portfolio/list.html', ctx)
