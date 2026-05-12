#!/bin/bash
set -e
echo "================================================"
echo "  NovaSysTech — Installation & Démarrage"
echo "================================================"

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python manage.py makemigrations core services blog portfolio faq
python manage.py migrate

python manage.py loaddata services/fixtures/services.json
python manage.py loaddata core/fixtures/temoignages.json
python manage.py loaddata faq/fixtures/faq.json
python manage.py loaddata portfolio/fixtures/portfolio.json
python manage.py loaddata blog/fixtures/blog.json

echo ""
echo "Création du compte administrateur :"
python manage.py createsuperuser

echo ""
echo "================================================"
echo "  ✅ Installation terminée !"
echo "  Admin : http://127.0.0.1:8000/admin/"
echo "  Site  : http://127.0.0.1:8000/"
echo "================================================"
python manage.py runserver
