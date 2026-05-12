from django.contrib import admin
from django.utils.html import format_html
from .models import Projet

@admin.register(Projet)
class ProjetAdmin(admin.ModelAdmin):
    list_display = ['ordre', 'titre', 'client', 'categorie_badge', 'est_publie']
    list_editable = ['est_publie', 'ordre']
    list_display_links = ['titre']
    prepopulated_fields = {'slug': ('titre',)}
    list_filter = ['categorie', 'est_publie']
    search_fields = ['titre', 'client', 'description']

    def categorie_badge(self, obj):
        colors = {'cctv':'#1A4A72','reseaux':'#16A34A','maintenance':'#E87722','cloud':'#7C3AED','alarmes':'#DC2626','formation':'#0891B2'}
        color = colors.get(obj.categorie, '#6B7280')
        return format_html('<span style="background:{};color:white;padding:2px 10px;border-radius:10px;font-size:11px">{}</span>', color, obj.get_categorie_display())
    categorie_badge.short_description = 'Catégorie'
