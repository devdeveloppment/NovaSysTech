import requests
import logging
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from django.views.decorators.http import require_POST
from django.utils import timezone

logger = logging.getLogger('django.core.mail')

from .models import Temoignage, DemandeDevis, MessageContact, NewsletterAbonne
from services.models import Service
from portfolio.models import Projet
from blog.models import Article


def verify_recaptcha(token):
    """Verify reCAPTCHA v2/v3 token with Google."""
    try:
        r = requests.post(settings.RECAPTCHA_VERIFY_URL if hasattr(settings, 'RECAPTCHA_VERIFY_URL') else
                          'https://www.google.com/recaptcha/api/siteverify',
                          data={'secret': settings.RECAPTCHA_PRIVATE_KEY, 'response': token}, timeout=5)
        result = r.json()
        return result.get('success', False)
    except Exception:
        return True  # En cas d'erreur réseau, on laisse passer


def send_devis_emails(devis):
    """Send confirmation email to client + notification to NST."""
    # Email to NST
    subject_nst = f"[NST] Nouvelle demande de devis — {devis.nom_complet}"
    body_nst = f"""
Nouvelle demande de devis reçue sur le site NovaSysTech.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  INFORMATIONS CLIENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Nom complet  : {devis.nom_complet}
Email        : {devis.email}
Téléphone    : {devis.telephone}
Entreprise   : {devis.entreprise or 'Non renseigné'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  DÉTAILS DU PROJET
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Service      : {devis.get_service_display()}
Budget       : {devis.get_budget_display()}
Délai        : {devis.get_delai_display()}

Description :
{devis.description}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reçu le : {devis.created_at.strftime('%d/%m/%Y à %H:%M')}
Admin  : https://votre-domaine.com/admin/core/demandedevis/
"""
    try:
        msg = EmailMessage(
            subject=subject_nst,
            body=body_nst,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.NST_OWNER_EMAIL],
            reply_to=[devis.email]
        )
        msg.send()
        logger.info(f"Email devis envoyé à {settings.NST_EMAILS}")
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi du devis à NST: {e}")

    # Confirmation email to client
    subject_client = "✅ NovaSysTech — Votre demande de devis a été reçue"
    body_client = f"""
Bonjour {devis.nom_complet},

Merci d'avoir contacté NovaSysTech !

Nous avons bien reçu votre demande de devis pour : {devis.get_service_display()}.

Notre équipe d'experts va analyser votre besoin et vous recontacter dans les prochaines 24 heures ouvrables.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  RÉCAPITULATIF DE VOTRE DEMANDE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Service demandé : {devis.get_service_display()}
Budget estimé   : {devis.get_budget_display()}
Délai souhaité  : {devis.get_delai_display()}

En cas d'urgence, contactez-nous directement :
📞 {settings.PHONE_1}
📞 {settings.PHONE_2}
💬 WhatsApp : https://wa.me/{settings.WHATSAPP_NUMBER}

Cordialement,
L'équipe NovaSysTech
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NovaSysTech (NST) — IT Solution For All
Agoè Assiyéyé, derrière Station Cap Togo, Lomé, Togo
{settings.SITE_URL}
"""
    try:
        msg = EmailMessage(
            subject=subject_client,
            body=body_client,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[devis.email],
            reply_to=[settings.NST_OWNER_EMAIL]
        )
        msg.send()
        logger.info(f"Email de confirmation envoyé à {devis.email}")
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi du devis à {devis.email}: {e}")


def send_contact_email(msg):
    """Send contact message notification to NST + confirmation to client."""
    # Email to NST
    subject = f"[NST Contact] {msg.sujet} — {msg.nom}"
    body = f"""
Nouveau message de contact reçu sur NovaSysTech.

De      : {msg.nom}
Email   : {msg.email}
Tél     : {msg.telephone or 'Non renseigné'}
Sujet   : {msg.sujet}

Message :
{msg.message}

━━━━━━━━━━━━━━━━
Répondre à : {msg.email}
"""
    try:
        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.NST_OWNER_EMAIL],
            reply_to=[msg.email]
        )
        email.send()
        logger.info(f"Email de contact reçu de {msg.email}")
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi du message de contact: {e}")

    # Confirmation email to client
    subject_client = "✅ NovaSysTech — Votre message a été reçu"
    body_client = f"""
Bonjour {msg.nom},

Merci d'avoir contacté NovaSysTech !

Nous avons bien reçu votre message avec le sujet : "{msg.sujet}".

Notre équipe va traiter votre demande et vous recontacter dans les prochaines 24 heures ouvrables.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  VOS INFORMATIONS DE CONTACT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Nom       : {msg.nom}
Email     : {msg.email}
Téléphone : {msg.telephone or 'Non fourni'}

En cas d'urgence, contactez-nous directement :
📞 {settings.PHONE_1}
📞 {settings.PHONE_2}
💬 WhatsApp : https://wa.me/{settings.WHATSAPP_NUMBER}

Cordialement,
L'équipe NovaSysTech
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NovaSysTech (NST) — IT Solution For All
Agoè Assiyéyé, derrière Station Cap Togo, Lomé, Togo
{settings.SITE_URL}
"""
    try:
        email_client = EmailMessage(
            subject=subject_client,
            body=body_client,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[msg.email],
            reply_to=[settings.NST_OWNER_EMAIL]
        )
        email_client.send()
        logger.info(f"Email de confirmation envoyé à {msg.email}")
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi de la confirmation à {msg.email}: {e}")


def send_response_email(msg, reponse):
    """Send response email to client."""
    subject = f"✉️ NovaSysTech — Réponse à votre message : {msg.sujet}"
    body = f"""
Bonjour {msg.nom},

Merci pour votre message. Voici notre réponse :

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  VOTRE MESSAGE (Sujet: {msg.sujet})
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{msg.message}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  NOTRE RÉPONSE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{reponse}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Si vous avez d'autres questions, n'hésitez pas à nous recontacter.

En cas d'urgence :
📞 {settings.PHONE_1}
📞 {settings.PHONE_2}
💬 WhatsApp : https://wa.me/{settings.WHATSAPP_NUMBER}

Cordialement,
L'équipe NovaSysTech
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NovaSysTech (NST) — IT Solution For All
Agoè Assiyéyé, derrière Station Cap Togo, Lomé, Togo
{settings.SITE_URL}
"""
    try:
        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[msg.email],
            reply_to=[settings.NST_OWNER_EMAIL]
        )
        email.send()
        logger.info(f"Email de réponse envoyé à {msg.email}")
        return True
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi de la réponse à {msg.email}: {e}")
        return False



def index(request):
    temoignages = Temoignage.objects.filter(est_publie=True)[:3]
    services = Service.objects.filter(est_actif=True).order_by('ordre')
    projets = Projet.objects.filter(est_publie=True)[:3]
    articles = Article.objects.filter(est_publie=True)[:3]
    ctx = {'temoignages': temoignages, 'services': services,
           'projets': projets, 'articles': articles, 'page': 'accueil'}
    return render(request, 'core/index.html', ctx)


def about(request):
    return render(request, 'core/about.html', {'page': 'about'})


def contact(request):
    if request.method == 'POST':
        nom = request.POST.get('nom', '').strip()
        email = request.POST.get('email', '').strip()
        telephone = request.POST.get('telephone', '').strip()
        sujet = request.POST.get('sujet', '').strip()
        message_text = request.POST.get('message', '').strip()
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if not all([nom, email, sujet, message_text]):
            if is_ajax:
                return JsonResponse({'success': False, 'message': 'Veuillez remplir tous les champs obligatoires.'})
            messages.error(request, 'Veuillez remplir tous les champs.')
            return redirect('contact')

        msg = MessageContact.objects.create(
            nom=nom, email=email, telephone=telephone, sujet=sujet, message=message_text)
        send_contact_email(msg)

        if is_ajax:
            return JsonResponse({'success': True, 'message': 'Message envoyé avec succès ! Nous vous répondrons sous 24h.'})
        messages.success(request, 'Votre message a été envoyé avec succès !')
        return redirect('contact')

    return render(request, 'core/contact.html', {'page': 'contact'})


def devis(request):
    services = Service.objects.filter(est_actif=True).order_by('ordre')
    temoignage = Temoignage.objects.filter(est_publie=True).first()

    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        nom_complet = request.POST.get('nom_complet', '').strip()
        email = request.POST.get('email', '').strip()
        telephone = request.POST.get('telephone', '').strip()
        entreprise = request.POST.get('entreprise', '').strip()
        service = request.POST.get('service', '').strip()
        description = request.POST.get('description', '').strip()
        budget = request.POST.get('budget', 'nd')
        delai = request.POST.get('delai', 'flexible')

        if not all([nom_complet, email, telephone, service, description]):
            if is_ajax:
                return JsonResponse({'success': False, 'message': 'Veuillez remplir tous les champs obligatoires.'})
            messages.error(request, 'Veuillez remplir tous les champs.')
            return redirect('devis')

        ip = request.META.get('REMOTE_ADDR')
        dv = DemandeDevis.objects.create(
            nom_complet=nom_complet, email=email, telephone=telephone,
            entreprise=entreprise, service=service, description=description,
            budget=budget, delai=delai, ip_address=ip)
        send_devis_emails(dv)

        if is_ajax:
            return JsonResponse({'success': True, 'message': 'Demande envoyée avec succès ! Nous vous contactons sous 24h. Un email de confirmation vous a été envoyé.'})
        messages.success(request, 'Votre demande a été envoyée ! Nous vous contactons sous 24h.')
        return redirect('devis')

    ctx = {'page': 'devis', 'services': services, 'temoignage': temoignage}
    return render(request, 'core/devis.html', ctx)


@require_POST
def newsletter(request):
    email = request.POST.get('email', '').strip()
    if not email or '@' not in email:
        return JsonResponse({'success': False, 'message': 'Adresse email invalide.'})
    obj, created = NewsletterAbonne.objects.get_or_create(email=email)
    if created:
        return JsonResponse({'success': True, 'message': 'Merci ! Vous êtes maintenant abonné(e) à notre newsletter.'})
    return JsonResponse({'success': False, 'message': 'Cette adresse est déjà abonnée.'})


def mentions_legales(request):
    return render(request, 'core/mentions.html')
