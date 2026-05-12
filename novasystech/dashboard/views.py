from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.db.models import Count, Q
from django.contrib import messages as django_messages
from datetime import timedelta
import csv
import json

from core.models import DemandeDevis, MessageContact, NewsletterAbonne, Temoignage
from core.views import send_response_email
from services.models import Service
from portfolio.models import Projet
from blog.models import Article, Categorie
from faq.models import FAQ


def dashboard_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard_home')
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            return redirect('dashboard_home')
        error = 'Identifiants incorrects ou accès non autorisé.'
    return render(request, 'dashboard/login.html', {'error': error})


def dashboard_logout(request):
    logout(request)
    return redirect('dashboard_login')


@login_required(login_url='/dashboard/login/')
def dashboard_home(request):
    now = timezone.now()
    last_30 = now - timedelta(days=30)
    last_7 = now - timedelta(days=7)

    # Stats principales
    total_devis = DemandeDevis.objects.count()
    nouveaux_devis = DemandeDevis.objects.filter(statut='nouveau').count()
    devis_ce_mois = DemandeDevis.objects.filter(created_at__gte=last_30).count()
    devis_cette_semaine = DemandeDevis.objects.filter(created_at__gte=last_7).count()

    total_messages = MessageContact.objects.count()
    messages_non_lus = MessageContact.objects.filter(lu=False).count()

    total_abonnes = NewsletterAbonne.objects.filter(actif=True).count()
    total_projets = Projet.objects.filter(est_publie=True).count()
    total_articles = Article.objects.filter(est_publie=True).count()
    total_services = Service.objects.filter(est_actif=True).count()

    # Dernières demandes de devis
    derniers_devis = DemandeDevis.objects.order_by('-created_at')[:8]

    # Derniers messages
    derniers_messages = MessageContact.objects.order_by('-created_at')[:5]

    # Stats devis par service
    devis_par_service = DemandeDevis.objects.values('service').annotate(
        total=Count('id')).order_by('-total')[:6]

    # Devis par statut
    devis_par_statut = {
        'nouveau': DemandeDevis.objects.filter(statut='nouveau').count(),
        'en_cours': DemandeDevis.objects.filter(statut='en_cours').count(),
        'traite': DemandeDevis.objects.filter(statut='traite').count(),
        'archive': DemandeDevis.objects.filter(statut='archive').count(),
    }

    # Activité 7 derniers jours
    activite = []
    for i in range(6, -1, -1):
        day = now - timedelta(days=i)
        count = DemandeDevis.objects.filter(
            created_at__date=day.date()).count()
        activite.append({'jour': day.strftime('%a'), 'count': count})

    ctx = {
        'page': 'home',
        'total_devis': total_devis,
        'nouveaux_devis': nouveaux_devis,
        'devis_ce_mois': devis_ce_mois,
        'devis_cette_semaine': devis_cette_semaine,
        'total_messages': total_messages,
        'messages_non_lus': messages_non_lus,
        'total_abonnes': total_abonnes,
        'total_projets': total_projets,
        'total_articles': total_articles,
        'total_services': total_services,
        'derniers_devis': derniers_devis,
        'derniers_messages': derniers_messages,
        'devis_par_service': devis_par_service,
        'devis_par_statut': devis_par_statut,
        'activite': json.dumps(activite),
    }
    return render(request, 'dashboard/home.html', ctx)


@login_required(login_url='/dashboard/login/')
def devis_list(request):
    qs = DemandeDevis.objects.order_by('-created_at')
    # Filtres
    statut = request.GET.get('statut', '')
    service = request.GET.get('service', '')
    search = request.GET.get('q', '')
    if statut:
        qs = qs.filter(statut=statut)
    if service:
        qs = qs.filter(service=service)
    if search:
        qs = qs.filter(
            Q(nom_complet__icontains=search) |
            Q(email__icontains=search) |
            Q(telephone__icontains=search) |
            Q(entreprise__icontains=search)
        )
    ctx = {
        'page': 'devis',
        'devis_list': qs,
        'statut_filter': statut,
        'service_filter': service,
        'search': search,
        'total': qs.count(),
        'statuts': DemandeDevis.STATUTS,
        'services': DemandeDevis.SERVICES,
    }
    return render(request, 'dashboard/devis.html', ctx)


@login_required(login_url='/dashboard/login/')
def devis_detail(request, pk):
    dv = get_object_or_404(DemandeDevis, pk=pk)
    if request.method == 'POST':
        dv.statut = request.POST.get('statut', dv.statut)
        dv.save()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'statut': dv.get_statut_display()})
        return redirect('devis_list')
    return render(request, 'dashboard/devis_detail.html', {'page': 'devis', 'dv': dv})


@login_required(login_url='/dashboard/login/')
def devis_export(request):
    qs = DemandeDevis.objects.order_by('-created_at')
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="devis_novasystech.csv"'
    response.write('\ufeff')
    writer = csv.writer(response)
    writer.writerow(['Date', 'Nom', 'Email', 'Téléphone', 'Entreprise',
                     'Service', 'Budget', 'Délai', 'Description', 'Statut'])
    for d in qs:
        writer.writerow([
            d.created_at.strftime('%d/%m/%Y %H:%M'),
            d.nom_complet, d.email, d.telephone, d.entreprise,
            d.get_service_display(), d.get_budget_display(),
            d.get_delai_display(), d.description, d.get_statut_display()
        ])
    return response


@login_required(login_url='/dashboard/login/')
def messages_list(request):
    qs = MessageContact.objects.order_by('-created_at')
    search = request.GET.get('q', '')
    lu_filter = request.GET.get('lu', '')
    if search:
        qs = qs.filter(Q(nom__icontains=search) | Q(email__icontains=search) | Q(sujet__icontains=search))
    if lu_filter == '0':
        qs = qs.filter(lu=False)
    elif lu_filter == '1':
        qs = qs.filter(lu=True)
    ctx = {'page': 'messages', 'messages_list': qs, 'search': search,
           'lu_filter': lu_filter, 'non_lus': MessageContact.objects.filter(lu=False).count()}
    return render(request, 'dashboard/messages.html', ctx)


@login_required(login_url='/dashboard/login/')
def message_detail(request, pk):
    msg = get_object_or_404(MessageContact, pk=pk)
    msg.lu = True
    msg.save()
    return render(request, 'dashboard/message_detail.html', {'page': 'messages', 'msg': msg})


@login_required(login_url='/dashboard/login/')
def message_reply(request, pk):
    """Reply to a contact message."""
    msg = get_object_or_404(MessageContact, pk=pk)
    
    if request.method == 'POST':
        reponse = request.POST.get('reponse', '').strip()
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        if not reponse:
            if is_ajax:
                return JsonResponse({'success': False, 'message': 'La réponse ne peut pas être vide.'})
            django_messages.error(request, 'Veuillez entrer une réponse.')
            return redirect('message_detail', pk=pk)
        
        # Save the response
        msg.reponse = reponse
        msg.repondu_le = timezone.now()
        msg.save()
        
        # Send email to client
        email_sent = send_response_email(msg, reponse)
        
        if is_ajax:
            if email_sent:
                return JsonResponse({'success': True, 'message': 'Réponse envoyée avec succès au client !'})
            else:
                return JsonResponse({'success': False, 'message': 'Réponse enregistrée mais erreur lors de l\'envoi du mail.'})
        
        if email_sent:
            django_messages.success(request, 'Réponse envoyée avec succès au client !')
        else:
            django_messages.warning(request, 'Réponse enregistrée mais erreur lors de l\'envoi du mail.')
        
        return redirect('message_detail', pk=pk)
    
    return redirect('message_detail', pk=pk)



@login_required(login_url='/dashboard/login/')
def services_list(request):
    services = Service.objects.order_by('ordre')
    return render(request, 'dashboard/services.html', {'page': 'services', 'services': services})


@login_required(login_url='/dashboard/login/')
def temoignages_list(request):
    temoignages = Temoignage.objects.order_by('ordre')
    return render(request, 'dashboard/temoignages.html', {'page': 'temoignages', 'temoignages': temoignages})


@login_required(login_url='/dashboard/login/')
def projets_list(request):
    projets = Projet.objects.order_by('-date_realisation')
    return render(request, 'dashboard/projets.html', {'page': 'projets', 'projets': projets})


@login_required(login_url='/dashboard/login/')
def articles_list(request):
    articles = Article.objects.order_by('-date_publication')
    return render(request, 'dashboard/articles.html', {'page': 'articles', 'articles': articles})


@login_required(login_url='/dashboard/login/')
def newsletter_list(request):
    abonnes = NewsletterAbonne.objects.order_by('-created_at')
    return render(request, 'dashboard/newsletter.html',
                  {'page': 'newsletter', 'abonnes': abonnes,
                   'total': abonnes.count(), 'actifs': abonnes.filter(actif=True).count()})


@login_required(login_url='/dashboard/login/')
def update_statut(request, pk):
    """AJAX: update devis status"""
    if request.method == 'POST':
        dv = get_object_or_404(DemandeDevis, pk=pk)
        dv.statut = request.POST.get('statut', dv.statut)
        dv.save()
        return JsonResponse({'success': True, 'statut': dv.get_statut_display(), 'statut_key': dv.statut})
    return JsonResponse({'success': False})
