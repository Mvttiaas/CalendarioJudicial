from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import PlazoJudicial
from .utils.plazos import es_plazo_urgente, formatear_fecha_chilena


@admin.register(PlazoJudicial)
class PlazoJudicialAdmin(admin.ModelAdmin):
    """
    Configuración del admin para PlazoJudicial.
    Incluye filtros, búsqueda y acciones personalizadas.
    """
    
    list_display = [
        'id', 'tipo_documento', 'procedimiento', 'rol', 'rut_cliente',
        'fecha_inicio', 'fecha_vencimiento', 'dias_restantes_display',
        'estado_display', 'es_urgente_display', 'created_at'
    ]
    
    list_filter = [
        'tipo_documento', 'procedimiento', 'tipo_dia', 'estado',
        'fecha_inicio', 'fecha_vencimiento', 'created_at'
    ]
    
    search_fields = [
        'rol', 'rut_cliente', 'clave_cliente', 'tipo_documento', 'procedimiento',
        'observaciones'
    ]
    
    # list_editable = ['estado']  # Comentado temporalmente
    
    readonly_fields = [
        'fecha_vencimiento', 'created_at', 'updated_at',
        'dias_restantes_display', 'es_urgente_display'
    ]
    
    fieldsets = (
        ('Información Principal', {
            'fields': (
                'tipo_documento', 'procedimiento', 'dias_plazo', 'tipo_dia',
                'fecha_inicio', 'fecha_vencimiento'
            )
        }),
        ('Identificación', {
            'fields': ('rol', 'rut_cliente', 'clave_cliente')
        }),
        ('Estado y Control', {
            'fields': ('estado', 'observaciones', 'documento_adjunto')
        }),
        ('Información de Auditoría', {
            'fields': (
                'created_at', 'updated_at',
                'dias_restantes_display', 'es_urgente_display'
            ),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ['fecha_vencimiento', 'fecha_inicio']
    
    list_per_page = 25
    
    actions = ['marcar_como_corriendo', 'marcar_como_suspendido', 'actualizar_estados']
    
    def dias_restantes_display(self, obj):
        """
        Muestra los días restantes con colores según urgencia.
        """
        if not obj.fecha_vencimiento:
            return format_html('<span class="badge bg-secondary">N/A</span>')
        
        dias = obj.dias_restantes
        if dias is None:
            return format_html('<span class="badge bg-secondary">N/A</span>')
        
        if dias <= 0:
            return format_html('<span class="badge bg-danger">{} días</span>', dias)
        elif dias <= 3:
            return format_html('<span class="badge bg-warning">{} días</span>', dias)
        else:
            return format_html('<span class="badge bg-success">{} días</span>', dias)
    
    dias_restantes_display.short_description = 'Días Restantes'
    dias_restantes_display.admin_order_field = 'fecha_vencimiento'
    
    def estado_display(self, obj):
        """
        Muestra el estado con colores.
        """
        colores = {
            'pendiente': 'secondary',
            'esperando_proveido': 'warning',
            'corriendo': 'info',
            'suspendido': 'secondary',
            'vencido': 'danger',
        }
        
        color = colores.get(obj.estado, 'secondary')
        return format_html(
            '<span class="badge bg-{}">{}</span>',
            color, obj.get_estado_display()
        )
    
    estado_display.short_description = 'Estado'
    estado_display.admin_order_field = 'estado'
    
    def es_urgente_display(self, obj):
        """
        Indica si el plazo es urgente.
        """
        if not obj.fecha_vencimiento:
            return format_html('<span class="badge bg-secondary">N/A</span>')
        
        if es_plazo_urgente(obj.fecha_vencimiento):
            return format_html('<span class="badge bg-warning">⚠️ URGENTE</span>')
        else:
            return format_html('<span class="badge bg-success">✓ Normal</span>')
    
    es_urgente_display.short_description = 'Urgencia'
    
    def marcar_como_corriendo(self, request, queryset):
        """
        Acción para marcar plazos como corriendo.
        """
        actualizados = queryset.update(estado='corriendo')
        self.message_user(
            request,
            f'Se marcaron {actualizados} plazos como corriendo.'
        )
    
    marcar_como_corriendo.short_description = 'Marcar como corriendo'
    
    def marcar_como_suspendido(self, request, queryset):
        """
        Acción para marcar plazos como suspendidos.
        """
        actualizados = queryset.update(estado='suspendido')
        self.message_user(
            request,
            f'Se marcaron {actualizados} plazos como suspendidos.'
        )
    
    marcar_como_suspendido.short_description = 'Marcar como suspendidos'
    
    def actualizar_estados(self, request, queryset):
        """
        Acción para actualizar estados de plazos.
        """
        actualizados = 0
        for plazo in queryset:
            estado_anterior = plazo.estado
            plazo.actualizar_estado()
            if plazo.estado != estado_anterior:
                actualizados += 1
        
        self.message_user(
            request,
            f'Se actualizaron {actualizados} plazos.'
        )
    
    actualizar_estados.short_description = 'Actualizar estados'
    
    def get_queryset(self, request):
        """
        Optimiza las consultas del admin.
        """
        return super().get_queryset(request).select_related()
    
    class Media:
        css = {
            'all': ('admin/css/plazos_admin.css',)
        }
        js = ('admin/js/plazos_admin.js',)


# Configuración del sitio admin
admin.site.site_header = "Calendario Judicial - Administración"
admin.site.site_title = "Calendario Judicial"
admin.site.index_title = "Gestión de Plazos Judiciales"
