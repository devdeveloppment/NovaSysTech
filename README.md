# 🚀 NovaSysTech - Solutions Technologiques Innovantes

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0+-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

**NovaSysTech** est une plateforme web moderne et complète développée pour une entreprise de services technologiques basée à Lomé, Togo. Elle offre une vitrine professionnelle pour une large gamme de services allant de la maintenance informatique à l'intelligence artificielle.

---

## 📑 Sommaire
- [✨ Fonctionnalités](#-fonctionnalités)
- [🛠️ Stack Technique](#️-stack-technique)
- [🚀 Installation Rapide](#-installation-rapide)
- [📂 Structure du Projet](#-structure-du-projet)
- [🖥️ Aperçu des Services](#️-aperçu-des-services)
- [🔒 Administration](#-administration)
- [📧 Contact](#-contact)

---

## ✨ Fonctionnalités

- **🌐 Site Vitrine Responsive** : Design moderne optimisé pour mobile, tablette et desktop.
- **🛠️ Gestion de Services** : Présentation détaillée des expertises (IT, CCTV, Réseaux, Cloud, IA).
- **💼 Portfolio Dynamique** : Galerie des projets réalisés avec filtrage.
- **📝 Blog Intégré** : Partage d'actualités et d'articles techniques.
- **📊 Tableau de Bord Admin** : Interface personnalisée pour gérer les devis, messages, et contenus.
- **📩 Système de Devis & Contact** : Formulaires interactifs avec suivi en base de données.
- **❓ FAQ** : Section d'aide pour les clients.

---

## 🛠️ Stack Technique

- **Backend** : Django 5.0.x (Python)
- **Base de données** : SQLite (Développement) / PostgreSQL (Production recommandé)
- **Frontend** : HTML5, CSS3 (Vanilla), JavaScript, FontAwesome 6
- **Template Engine** : Django Templates
- **Gestion de contenu** : Django Admin Customisé

---

## 🚀 Installation Rapide

### Prérequis
- Python 3.10 ou supérieur
- Git

### Étapes d'installation

1. **Cloner le projet**
   ```bash
   git clone https://github.com/devdeveloppment/NovaSysTech.git
   cd NovaSysTech
   ```

2. **Lancer l'installation automatique** (Recommandé)
   ```bash
   cd novasystech
   bash setup.sh
   ```

   *Ou installation manuelle :*

   ```bash
   # Création de l'environnement virtuel
   python -m venv venv
   source venv/Scripts/activate  # Sur Windows: venv\Scripts\activate

   # Installation des dépendances
   pip install -r requirements.txt

   # Migrations et données initiales
   python manage.py makemigrations core services blog portfolio faq
   python manage.py migrate
   python manage.py loaddata services/fixtures/services.json core/fixtures/temoignages.json faq/fixtures/faq.json portfolio/fixtures/portfolio.json blog/fixtures/blog.json

   # Lancement
   python manage.py runserver
   ```

---

## 🖥️ Aperçu des Services

| Service | Description |
| :--- | :--- |
| **Maintenance IT** | Diagnostic, réparation et optimisation de parcs informatiques. |
| **Vidéosurveillance (CCTV)** | Installation et configuration de systèmes de sécurité avancés. |
| **Réseaux & WiFi** | Déploiement de solutions réseau haut débit (Câblage, WiFi 6). |
| **Alarmes & Accès** | Systèmes anti-intrusion et contrôle d'accès biométrique. |
| **Cloud & IA** | Transformation digitale et intégration de solutions d'IA. |
| **Formation** | Accompagnement et certification sur les technologies clés. |

---

## 🔒 Administration

L'interface d'administration est accessible via `/admin/`. Elle permet de :
- Gérer les articles du blog et les projets du portfolio.
- Répondre aux demandes de devis et messages de contact.
- Mettre à jour les témoignages et la FAQ.

---

## 📧 Contact

**NovaSysTech**
- 📍 **Adresse** : Agoè Assiyéyé, derrière Station Cap Togo, Lomé, Togo
- 📞 **Téléphone** : [+228 79 92 81 81](tel:+22879928181) / [+228 70 30 79 68](tel:+22870307968)
- ✉️ **Email** : [contact@novasystechn.com](mailto:contact@novasystechn.com)
- 🌐 **Site Web** : [www.novasystechn.com](http://www.novasystechn.com)

---
*Développé avec ❤️ par l'équipe NovaSysTech.*
