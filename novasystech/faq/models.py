from django.db import models

class FAQ(models.Model):
    CATEGORIES = [
        ('general', 'Général'),
        ('services', 'Services'),
        ('devis', 'Devis & Tarifs'),
    ]
    question = models.CharField(max_length=400)
    reponse = models.TextField()
    categorie = models.CharField(max_length=50, choices=CATEGORIES, default='general')
    ordre = models.IntegerField(default=0)
    est_actif = models.BooleanField(default=True)

    class Meta:
        ordering = ['categorie', 'ordre']
        verbose_name = 'FAQ'

    def __str__(self):
        return self.question
