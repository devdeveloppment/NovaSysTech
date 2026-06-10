from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.utils.text import slugify
from .models import Projet

DEMO_PROJETS = [
    ('https://images.unsplash.com/photo-1557597774-9d273605dfa9?w=600&q=80', 'Banque Régionale', 'cctv', 'Déploiement d\'un système de surveillance IP intelligent HD.'),
    ('https://images.unsplash.com/photo-1544197150-b99a580bb7a8?w=600&q=80', 'Groupe Bancaire International', 'cloud', 'Migration hybride vers Azure et optimisation des infrastructures serveurs.'),
    ('https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=600&q=80', 'Port Industriel d\'Afrique', 'reseaux', 'Refonte complète de l\'infrastructure fibre optique et wifi industriel.'),
    ('https://images.unsplash.com/photo-1581092160562-40aa08e78837?w=600&q=80', 'Opérateur Télécom National', 'maintenance', 'Contrat de maintenance préventive du parc informatique.'),
    ('https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=600&q=80', 'Institution Gouvernementale', 'maintenance', 'Audit de sécurité pour la digitalisation des services publics.'),
    ('https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=600&q=80', 'Campus Universitaire', 'reseaux', 'Extension backbone réseau pour connexions simultanées.'),
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

def portfolio_detail(request, slug):
    try:
        projet = Projet.objects.get(slug=slug, est_publie=True)
        is_demo = False
    except Projet.DoesNotExist:
        # Check in demo projects
        projet_demo = next((p for p in DEMO_PROJETS if slugify(p[1]) == slug), None)
        if not projet_demo:
            raise Http404("Réalisation introuvable")
        
        class FakeProjet:
            titre = projet_demo[1]
            description = projet_demo[3]
            categorie = projet_demo[2]
            client = "Client Confidentiel"
            def get_categorie_display(self):
                cats = dict(Projet.CATEGORIES)
                return cats.get(self.categorie, self.categorie)
            def image_url_fake(self):
                return projet_demo[0]
            
        projet = FakeProjet()
        is_demo = True

    return render(request, 'portfolio/detail.html', {'projet': projet, 'is_demo': is_demo})
