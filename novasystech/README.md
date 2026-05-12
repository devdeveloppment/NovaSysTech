# NovaSysTech — Site Web Complet

**Stack :** Django 5 · SQLite · HTML/CSS/JS · Font Awesome

## Démarrage rapide

```bash
bash setup.sh
```

Ou manuellement :

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations core services blog portfolio faq
python manage.py migrate
python manage.py loaddata services/fixtures/services.json
python manage.py loaddata core/fixtures/temoignages.json
python manage.py loaddata faq/fixtures/faq.json
python manage.py loaddata portfolio/fixtures/portfolio.json
python manage.py loaddata blog/fixtures/blog.json
python manage.py createsuperuser
python manage.py runserver
```

## Pages disponibles

| Page | URL |
|------|-----|
| Accueil | http://127.0.0.1:8000/ |
| À Propos | http://127.0.0.1:8000/a-propos/ |
| Services | http://127.0.0.1:8000/services/ |
| Maintenance IT | http://127.0.0.1:8000/services/maintenance-informatique/ |
| CCTV | http://127.0.0.1:8000/services/videosurveillance-cctv/ |
| Réseaux | http://127.0.0.1:8000/services/reseaux-wifi-cable/ |
| Alarmes | http://127.0.0.1:8000/services/alarmes-controle-acces/ |
| Cloud & IA | http://127.0.0.1:8000/services/cloud-intelligence-artificielle/ |
| Formation | http://127.0.0.1:8000/services/formation-certification/ |
| Portfolio | http://127.0.0.1:8000/portfolio/ |
| FAQ | http://127.0.0.1:8000/faq/ |
| Blog | http://127.0.0.1:8000/blog/ |
| Devis | http://127.0.0.1:8000/demande-devis/ |
| Contact | http://127.0.0.1:8000/contact/ |
| Admin | http://127.0.0.1:8000/admin/ |

## Configuration production

Dans `novasystech/settings.py` :
- `DEBUG = False`
- Remplacer `EMAIL_BACKEND` par SMTP réel
- Définir `SECRET_KEY` unique et sécurisée
- Configurer `ALLOWED_HOSTS`

## Admin par défaut (créé par setup.sh)
Choisissez vous-même votre login lors de l'installation.

## Contact NST
- Tél : +228 79 92 81 81 / +228 70 30 79 68
- Email : contact@novasystechn.com
- Adresse : Agoè Assiyéyé, derrière Station Cap Togo, Lomé
