from django.db import models

class Temoignage(models.Model):
    nom = models.CharField(max_length=100)
    poste = models.CharField(max_length=150)
    entreprise = models.CharField(max_length=150, blank=True)
    photo = models.ImageField(upload_to='temoignages/', blank=True, null=True)
    texte = models.TextField()
    note = models.IntegerField(default=5, choices=[(i,i) for i in range(1,6)])
    est_publie = models.BooleanField(default=True)
    ordre = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['ordre', '-created_at']
        verbose_name = 'Témoignage'

    def __str__(self):
        return f"{self.nom} — {self.entreprise}"

class DemandeDevis(models.Model):
    SERVICES = [
        ('maintenance', 'Maintenance Informatique'),
        ('cctv', 'Vidéosurveillance (CCTV)'),
        ('reseaux', 'Réseaux Wi-Fi & Câblé'),
        ('alarmes', 'Alarmes & Contrôle d\'accès'),
        ('cloud_ia', 'Cloud & Intelligence Artificielle'),
        ('formation', 'Formation & Certification'),
        ('autre', 'Autre'),
    ]
    BUDGETS = [
        ('lt100', '< 100 000 FCFA'),
        ('100_500', '100 000 – 500 000 FCFA'),
        ('500_1m', '500 000 – 2 000 000 FCFA'),
        ('gt2m', '+ 2 000 000 FCFA'),
        ('nd', 'Non défini'),
    ]
    DELAIS = [
        ('urgent', 'Urgent (Moins de 1 mois)'),
        ('1_3m', '1 à 3 mois'),
        ('3_6m', '3 à 6 mois'),
        ('flexible', 'Flexible'),
    ]
    STATUTS = [
        ('nouveau', 'Nouveau'),
        ('en_cours', 'En cours'),
        ('traite', 'Traité'),
        ('archive', 'Archivé'),
    ]

    nom_complet = models.CharField(max_length=200)
    email = models.EmailField()
    telephone = models.CharField(max_length=30)
    entreprise = models.CharField(max_length=200, blank=True)
    service = models.CharField(max_length=50, choices=SERVICES)
    description = models.TextField()
    budget = models.CharField(max_length=20, choices=BUDGETS, default='nd')
    delai = models.CharField(max_length=20, choices=DELAIS, default='flexible')
    statut = models.CharField(max_length=20, choices=STATUTS, default='nouveau')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Demande de Devis'
        verbose_name_plural = 'Demandes de Devis'

    def __str__(self):
        return f"{self.nom_complet} — {self.get_service_display()} ({self.created_at.strftime('%d/%m/%Y')})"

class MessageContact(models.Model):
    nom = models.CharField(max_length=200)
    email = models.EmailField()
    telephone = models.CharField(max_length=30, blank=True)
    sujet = models.CharField(max_length=300)
    message = models.TextField()
    lu = models.BooleanField(default=False)
    reponse = models.TextField(blank=True, null=True)
    repondu_le = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Message Contact'

    def __str__(self):
        return f"{self.nom} — {self.sujet}"
    
    @property
    def a_reponse(self):
        return bool(self.reponse)

class NewsletterAbonne(models.Model):
    email = models.EmailField(unique=True)
    actif = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Abonné Newsletter'

    def __str__(self):
        return self.email
