from django.contrib import admin
from django.utils.html import format_html
from .models import Service

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['ordre', 'icone_preview', 'nom', 'slug', 'est_actif']
    list_editable = ['ordre', 'est_actif']
    list_display_links = ['nom']
    prepopulated_fields = {'slug': ('nom',)}
    search_fields = ['nom', 'description_courte']
    list_filter = ['est_actif']

    fieldsets = (
        ('📋 Informations principales', {
            'fields': ('nom', 'slug', 'icone', 'ordre', 'est_actif')
        }),
        ('📝 Contenu', {
            'fields': ('description_courte', 'description_longue', 'image_hero')
        }),
        ('✅ Features & Avantages', {
            'fields': ('features', 'avantages'),
            'description': 'Une entrée par ligne'
        }),
        ('🔍 SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
    )

    def icone_preview(self, obj):
        icons = {
            'wrench': '🔧', 'video': '📹', 'wifi': '📡',
            'shield': '🔒', 'cloud': '☁️', 'graduation-cap': '🎓'
        }
        return format_html('<span style="font-size:20px">{}</span>', icons.get(obj.icone, '⚙️'))
    icone_preview.short_description = ''
