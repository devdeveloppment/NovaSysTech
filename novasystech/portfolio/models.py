from django.db import models
from django.utils.text import slugify

class Projet(models.Model):
    CATEGORIES = [
        ('cctv', 'CCTV & Sécurité'),
        ('reseaux', 'Réseaux'),
        ('maintenance', 'Maintenance'),
        ('cloud', 'Cloud'),
        ('alarmes', 'Alarmes'),
        ('formation', 'Formation'),
    ]
    titre = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    categorie = models.CharField(max_length=50, choices=CATEGORIES, default='cctv')
    client = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='portfolio/', blank=True, null=True)
    date_realisation = models.DateField(null=True, blank=True)
    est_publie = models.BooleanField(default=True)
    ordre = models.IntegerField(default=0)

    class Meta:
        ordering = ['ordre', '-date_realisation']
        verbose_name = 'Projet Portfolio'

    def __str__(self):
        return self.titre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
        super().save(*args, **kwargs)
