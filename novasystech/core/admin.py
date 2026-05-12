from django.contrib import admin
from django.utils.html import format_html
from django.http import HttpResponse
import csv
from .models import Temoignage, DemandeDevis, MessageContact, NewsletterAbonne

admin.site.site_header = "NovaSysTech — Administration"
admin.site.site_title = "NST Admin"
admin.site.index_title = "Tableau de bord NovaSysTech"

def export_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="export_nst.csv"'
    response.write('\ufeff')
    fields = [f.name for f in queryset.model._meta.fields]
    writer = csv.writer(response)
    writer.writerow(fields)
    for obj in queryset:
        writer.writerow([getattr(obj, f) for f in fields])
    return response
export_csv.short_description = "📥 Exporter en CSV"

@admin.register(DemandeDevis)
class DemandeDevisAdmin(admin.ModelAdmin):
    list_display = ['nom_complet', 'telephone', 'email', 'service_badge', 'budget', 'statut_badge', 'created_at', 'statut']
    list_filter = ['statut', 'service', 'budget', 'created_at']
    list_editable = ['statut']
    search_fields = ['nom_complet', 'email', 'telephone', 'entreprise']
    readonly_fields = ['ip_address', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    actions = [export_csv]
    ordering = ['-created_at']
    fieldsets = (
        ('👤 Informations Client', {'fields': ('nom_complet', 'email', 'telephone', 'entreprise')}),
        ('📋 Projet', {'fields': ('service', 'description', 'budget', 'delai')}),
        ('⚙️ Gestion', {'fields': ('statut', 'ip_address', 'created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
    def service_badge(self, obj):
        colors = {'maintenance':'#E87722','cctv':'#1A4A72','reseaux':'#16A34A','alarmes':'#DC2626','cloud_ia':'#7C3AED','formation':'#0891B2'}
        c = colors.get(obj.service, '#6B7280')
        return format_html('<span style="background:{};color:white;padding:2px 8px;border-radius:10px;font-size:11px;font-weight:600">{}</span>', c, obj.get_service_display())
    service_badge.short_description = 'Service'
    def statut_badge(self, obj):
        colors = {'nouveau':'#E87722','en_cours':'#0891B2','traite':'#16A34A','archive':'#6B7280'}
        c = colors.get(obj.statut, '#6B7280')
        return format_html('<span style="background:{};color:white;padding:2px 8px;border-radius:10px;font-size:11px;font-weight:600">{}</span>', c, obj.get_statut_display())
    statut_badge.short_description = 'État'

@admin.register(MessageContact)
class MessageContactAdmin(admin.ModelAdmin):
    list_display = ['nom', 'email', 'sujet', 'lu_badge', 'lu', 'created_at']
    list_filter = ['lu', 'created_at']
    list_editable = ['lu']
    search_fields = ['nom', 'email', 'sujet']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    def lu_badge(self, obj):
        if obj.lu:
            return format_html('<span style="color:#16A34A;font-weight:700">✓ Lu</span>')
        return format_html('<span style="color:#E87722;font-weight:700">● Non lu</span>')
    lu_badge.short_description = 'État'

@admin.register(Temoignage)
class TemoignageAdmin(admin.ModelAdmin):
    list_display = ['nom', 'entreprise', 'note_stars', 'est_publie', 'ordre']
    list_editable = ['est_publie', 'ordre']
    list_filter = ['est_publie', 'note']
    def note_stars(self, obj):
        return format_html('<span title="{}/5">{}</span>', obj.note, '⭐' * obj.note)
    note_stars.short_description = 'Note'

@admin.register(NewsletterAbonne)
class NewsletterAbonneAdmin(admin.ModelAdmin):
    list_display = ['email', 'actif', 'created_at']
    list_editable = ['actif']
    list_filter = ['actif']
    actions = [export_csv]
