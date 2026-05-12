from django.contrib import admin
from django.utils.html import format_html
from .models import Article, Categorie

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ['nom', 'slug', 'couleur_preview']
    prepopulated_fields = {'slug': ('nom',)}

    def couleur_preview(self, obj):
        return format_html('<span style="background:{};padding:4px 16px;border-radius:8px;color:white;font-weight:600">{}</span>', obj.couleur, obj.couleur)
    couleur_preview.short_description = 'Couleur'

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['titre', 'categorie', 'auteur', 'temps_lecture', 'est_publie', 'est_une', 'date_publication']
    list_editable = ['est_publie', 'est_une']
    list_filter = ['est_publie', 'est_une', 'categorie']
    prepopulated_fields = {'slug': ('titre',)}
    search_fields = ['titre', 'auteur', 'tags', 'extrait']
    date_hierarchy = 'date_publication'
    fieldsets = (
        ('📋 Informations', {'fields': ('titre', 'slug', 'categorie', 'auteur', 'temps_lecture', 'est_publie', 'est_une')}),
        ('🖼️ Visuel', {'fields': ('image_hero',)}),
        ('📝 Contenu', {'fields': ('extrait', 'contenu', 'tags')}),
        ('🔍 SEO', {'fields': ('meta_title', 'meta_description'), 'classes': ('collapse',)}),
    )
