from django.contrib import admin
from .models import FAQ

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['ordre', 'question', 'categorie', 'est_actif']
    list_editable = ['ordre', 'est_actif']
    list_display_links = ['question']
    list_filter = ['categorie', 'est_actif']
    search_fields = ['question', 'reponse']
