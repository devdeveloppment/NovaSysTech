from django.db import models
from django.utils.text import slugify

class Categorie(models.Model):
    nom = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    couleur = models.CharField(max_length=7, default='#E87722')

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)

class Article(models.Model):
    titre = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, max_length=300)
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True, blank=True)
    auteur = models.CharField(max_length=100, default='Équipe NST')
    image_hero = models.ImageField(upload_to='blog/', blank=True, null=True)
    extrait = models.TextField(max_length=400)
    contenu = models.TextField()
    tags = models.CharField(max_length=300, blank=True, help_text='Tags séparés par des virgules')
    est_publie = models.BooleanField(default=True)
    est_une = models.BooleanField(default=False, verbose_name='Article à la Une')
    temps_lecture = models.IntegerField(default=5, help_text='En minutes')
    date_publication = models.DateTimeField(auto_now_add=True)
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)

    class Meta:
        ordering = ['-date_publication']
        verbose_name = 'Article'

    def __str__(self):
        return self.titre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
        super().save(*args, **kwargs)

    def get_tags_list(self):
        return [t.strip() for t in self.tags.split(',') if t.strip()]
