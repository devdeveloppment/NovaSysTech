from django.db import models
from django.utils.text import slugify

class Service(models.Model):
    ICONES = [
        ('wrench', 'Maintenance'),
        ('video', 'CCTV'),
        ('wifi', 'Réseaux'),
        ('shield', 'Alarmes'),
        ('cloud', 'Cloud & IA'),
        ('graduation-cap', 'Formation'),
    ]

    nom = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    icone = models.CharField(max_length=50, default='wrench')
    description_courte = models.CharField(max_length=300)
    description_longue = models.TextField()
    image_hero = models.ImageField(upload_to='services/', blank=True, null=True)
    features = models.TextField(help_text='Une feature par ligne', blank=True)
    avantages = models.TextField(help_text='Un avantage par ligne', blank=True)
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    ordre = models.IntegerField(default=0)
    est_actif = models.BooleanField(default=True)

    class Meta:
        ordering = ['ordre']
        verbose_name = 'Service'

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)

    def get_features_list(self):
        return [f.strip() for f in self.features.split('\n') if f.strip()]

    def get_avantages_list(self):
        return [a.strip() for a in self.avantages.split('\n') if a.strip()]

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('service_detail', args=[self.slug])
