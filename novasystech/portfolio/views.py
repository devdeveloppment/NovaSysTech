from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.utils.text import slugify
from .models import Projet

DEMO_PROJETS = [
    ('https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=600&q=80', 'Déploiement Infrastructure Fibre', 'reseaux', 'Refonte complète de l\'infrastructure fibre optique et wifi industriel pour des connexions très haut débit.'),
    ('https://images.unsplash.com/photo-1629904853716-f0bc54198ce6?w=600&q=80', 'Contrat d\'Infogérance Globale', 'maintenance', 'Contrat de maintenance préventive et curative du parc informatique pour garantir la continuité des opérations.'),
    ('https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=600&q=80', 'Migration Data Center', 'cloud', 'Migration hybride vers le Cloud Azure et optimisation de l\'infrastructure des serveurs critiques.'),
    ('https://images.unsplash.com/photo-1582139329536-e7284fece509?w=600&q=80', 'Système de Détection Incendie', 'alarmes', 'Installation de détecteurs de fumée et de centrales d\'alarme pour une prévention incendie de pointe.'),
    ('https://images.unsplash.com/photo-1524178232363-1fb2b075b655?w=600&q=80', 'Académie Technologique', 'formation', 'Programme de formation certifiant en administration système et sécurité informatique pour les collaborateurs.'),
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
