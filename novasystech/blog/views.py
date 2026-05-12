from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Article, Categorie

DEMO_ARTICLES = [
    ('Comment l\'IA transforme les PME africaines en 2024','https://images.unsplash.com/photo-1677442135703-1787eea5ce01?w=400&q=80','Intelligence Artificielle',6),
    ('Migration vers le Cloud : Pourquoi maintenant ?','https://images.unsplash.com/photo-1544197150-b99a580bb7a8?w=400&q=80','Cloud Computing',5),
    ('Digitalisation du secteur bancaire au Togo','https://images.unsplash.com/photo-1563986768609-322da13575f3?w=400&q=80','Digitalisation',12),
    ('Top 5 des Frameworks Web en 2024','https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=400&q=80','Développement',8),
]

def blog_list(request):
    articles_qs = Article.objects.filter(est_publie=True)
    categorie_slug = request.GET.get('categorie')
    categorie_active = None
    if categorie_slug:
        categorie_active = get_object_or_404(Categorie, slug=categorie_slug)
        articles_qs = articles_qs.filter(categorie=categorie_active)
    une = Article.objects.filter(est_publie=True, est_une=True).first()
    if not une:
        une = Article.objects.filter(est_publie=True).first()
    rest = articles_qs.exclude(pk=une.pk) if une else articles_qs
    paginator = Paginator(rest, 4)
    page = request.GET.get('page', 1)
    articles_page = paginator.get_page(page)
    categories = Categorie.objects.all()
    populaires = Article.objects.filter(est_publie=True)[:3]
    total = Article.objects.filter(est_publie=True).count()
    ctx = {
        'page': 'blog',
        'une': une,
        'articles': articles_page,
        'categories': categories,
        'categorie_active': categorie_active,
        'populaires': populaires,
        'total_articles': total or 124,
        'demo_articles': DEMO_ARTICLES if total == 0 else [],
    }
    return render(request, 'blog/list.html', ctx)

def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, est_publie=True)
    recents = Article.objects.filter(est_publie=True).exclude(pk=article.pk)[:3]
    return render(request, 'blog/detail.html', {'article': article, 'recents': recents, 'page': 'blog'})
