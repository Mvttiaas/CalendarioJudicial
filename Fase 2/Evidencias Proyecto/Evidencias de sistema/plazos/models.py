from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from cryptography.fernet import Fernet
from django.conf import settings
from usuarios.models import Usuario

# Generar clave de encriptación si no existe
def get_encryption_key():
    key = getattr(settings, 'ENCRYPTION_KEY', None)
    if not key:
        key = Fernet.generate_key()
        # En producción, guardar esta clave de forma segura
    return key

class CodigoProcedimiento(models.Model):
    """Códigos de procedimiento civil con días automáticos"""
    TIPOS_DOCUMENTO = [
        ('demanda', 'Demanda'),
        ('contestacion', 'Contestación'),
        ('replica', 'Réplica'),
        ('duplica', 'Dúplica'),
        ('recurso_apelacion', 'Recurso de Apelación'),
        ('recurso_casacion', 'Recurso de Casación'),
        ('recurso_revision', 'Recurso de Revisión'),
        ('recurso_queja', 'Recurso de Queja'),
        ('recurso_proteccion', 'Recurso de Protección'),
        ('recurso_amparo', 'Recurso de Amparo'),
        ('recurso_amparo_economico', 'Recurso de Amparo Económico'),
        ('incidente', 'Incidente'),
        ('excepcion', 'Excepción'),
        ('reconvencion', 'Reconvención'),
        ('terceria', 'Tercería'),
        ('intervencion', 'Intervención'),
        ('desistimiento', 'Desistimiento'),
        ('allanamiento', 'Allanamiento'),
        ('transaccion', 'Transacción'),
        ('conciliacion', 'Conciliación'),
        ('mediacion', 'Mediación'),
        ('arbitraje', 'Arbitraje'),
        ('medida_cautelar', 'Medida Cautelar'),
        ('embargo', 'Embargo'),
        ('secuestro', 'Secuestro'),
        ('otro', 'Otro'),
    ]
    
    TIPOS_PROCEDIMIENTO = [
        ('ordinario', 'Procedimiento Ordinario'),
        ('sumario', 'Procedimiento Sumario'),
        ('ejecutivo', 'Procedimiento Ejecutivo'),
        ('monitorio', 'Procedimiento Monitorio'),
        ('laboral', 'Procedimiento Laboral'),
        ('familia', 'Procedimiento de Familia'),
        ('cobranza', 'Procedimiento de Cobranza'),
        ('violencia_intrafamiliar', 'Violencia Intrafamiliar'),
        ('alimentos', 'Alimentos'),
        ('divorcio', 'Divorcio'),
        ('cuidado_personal', 'Cuidado Personal'),
        ('relacion_directo', 'Relación Directo y Regular'),
        ('adopcion', 'Adopción'),
        ('menores', 'Menores'),
        ('adolescentes', 'Adolescentes'),
        ('penal', 'Procedimiento Penal'),
        ('administrativo', 'Procedimiento Administrativo'),
        ('tributario', 'Procedimiento Tributario'),
        ('otro', 'Otro'),
    ]
    
    TIPOS_DIA = [
        ('habil', 'Días Hábiles'),
        ('corrido', 'Días Corridos'),
    ]
    
    codigo = models.CharField(max_length=20, unique=True, help_text="Código del procedimiento (ej: ART. 254 CPC)")
    nombre = models.CharField(max_length=200, help_text="Nombre descriptivo del procedimiento")
    tipo_documento = models.CharField(max_length=30, choices=TIPOS_DOCUMENTO)
    tipo_procedimiento = models.CharField(max_length=30, choices=TIPOS_PROCEDIMIENTO)
    dias_plazo = models.IntegerField(validators=[MinValueValidator(1)], help_text="Días de plazo automático")
    tipo_dia = models.CharField(max_length=10, choices=TIPOS_DIA, default='habil')
    articulo_cpc = models.CharField(max_length=50, blank=True, help_text="Artículo del Código Procesal Civil")
    descripcion = models.TextField(blank=True, help_text="Descripción detallada del procedimiento")
    observaciones = models.TextField(blank=True, help_text="Observaciones especiales")
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Código de Procedimiento"
        verbose_name_plural = "Códigos de Procedimiento"
        ordering = ['codigo', 'tipo_documento']

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

class PlazoJudicial(models.Model):
    TIPOS_DOCUMENTO = [
        ('demanda', 'Demanda'),
        ('contestacion', 'Contestación'),
        ('replica', 'Réplica'),
        ('duplica', 'Dúplica'),
        ('recurso_apelacion', 'Recurso de Apelación'),
        ('recurso_casacion', 'Recurso de Casación'),
        ('recurso_revision', 'Recurso de Revisión'),
        ('recurso_queja', 'Recurso de Queja'),
        ('recurso_proteccion', 'Recurso de Protección'),
        ('recurso_amparo', 'Recurso de Amparo'),
        ('recurso_amparo_economico', 'Recurso de Amparo Económico'),
        ('incidente', 'Incidente'),
        ('excepcion', 'Excepción'),
        ('reconvencion', 'Reconvención'),
        ('terceria', 'Tercería'),
        ('intervencion', 'Intervención'),
        ('desistimiento', 'Desistimiento'),
        ('allanamiento', 'Allanamiento'),
        ('transaccion', 'Transacción'),
        ('conciliacion', 'Conciliación'),
        ('mediacion', 'Mediación'),
        ('arbitraje', 'Arbitraje'),
        ('medida_cautelar', 'Medida Cautelar'),
        ('embargo', 'Embargo'),
        ('secuestro', 'Secuestro'),
        ('otro', 'Otro'),
    ]
    
    TIPOS_PROCEDIMIENTO = [
        ('ordinario', 'Procedimiento Ordinario'),
        ('sumario', 'Procedimiento Sumario'),
        ('ejecutivo', 'Procedimiento Ejecutivo'),
        ('monitorio', 'Procedimiento Monitorio'),
        ('laboral', 'Procedimiento Laboral'),
        ('familia', 'Procedimiento de Familia'),
        ('cobranza', 'Procedimiento de Cobranza'),
        ('violencia_intrafamiliar', 'Violencia Intrafamiliar'),
        ('alimentos', 'Alimentos'),
        ('divorcio', 'Divorcio'),
        ('cuidado_personal', 'Cuidado Personal'),
        ('relacion_directo', 'Relación Directo y Regular'),
        ('adopcion', 'Adopción'),
        ('menores', 'Menores'),
        ('adolescentes', 'Adolescentes'),
        ('penal', 'Procedimiento Penal'),
        ('administrativo', 'Procedimiento Administrativo'),
        ('tributario', 'Procedimiento Tributario'),
        ('otro', 'Otro'),
    ]
    
    TIPOS_DIA = [
        ('habil', 'Días Hábiles'),
        ('corrido', 'Días Corridos'),
    ]
    
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('esperando_proveido', 'Esperando Proveído'),
        ('corriendo', 'Corriendo'),
        ('suspendido', 'Suspendido'),
        ('vencido', 'Vencido'),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='plazos')
    codigo_procedimiento = models.ForeignKey(CodigoProcedimiento, on_delete=models.SET_NULL, null=True, blank=True, 
                                           help_text="Código de procedimiento civil (opcional)")
    tipo_documento = models.CharField(max_length=30, choices=TIPOS_DOCUMENTO)
    procedimiento = models.CharField(max_length=30, choices=TIPOS_PROCEDIMIENTO)
    dias_plazo = models.IntegerField(validators=[MinValueValidator(1)])
    tipo_dia = models.CharField(max_length=10, choices=TIPOS_DIA)
    fecha_inicio = models.DateField()
    fecha_vencimiento = models.DateField()
    rol = models.CharField(max_length=20, blank=True, help_text="Serie de números para identificar el proceso")
    rut_cliente = models.CharField(max_length=20, blank=True, help_text="RUT del cliente")
    clave_cliente = models.CharField(max_length=200, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='corriendo')
    observaciones = models.TextField(blank=True, max_length=200)
    documento_adjunto = models.FileField(
        upload_to='documentos_plazos/%Y/%m/%d/',
        blank=True,
        null=True,
        help_text="Documento adjunto relacionado con el plazo"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Plazo Judicial"
        verbose_name_plural = "Plazos Judiciales"
        ordering = ['-fecha_vencimiento']

    def __str__(self):
        fecha_str = str(self.fecha_vencimiento) if self.fecha_vencimiento else "Sin fecha"
        return f"{self.get_tipo_documento_display()} - {self.get_procedimiento_display()} ({fecha_str})"

    def save(self, *args, **kwargs):
        # Si se selecciona un código de procedimiento, usar sus valores automáticos
        if self.codigo_procedimiento:
            self.tipo_documento = self.codigo_procedimiento.tipo_documento
            self.procedimiento = self.codigo_procedimiento.tipo_procedimiento
            self.dias_plazo = self.codigo_procedimiento.dias_plazo
            self.tipo_dia = self.codigo_procedimiento.tipo_dia
        
        # Calcular fecha de vencimiento automáticamente
        if self.fecha_inicio and self.dias_plazo and self.tipo_dia:
            from .utils.plazos import calcular_fecha_vencimiento
            self.fecha_vencimiento = calcular_fecha_vencimiento(
                self.fecha_inicio, 
                self.dias_plazo, 
                self.tipo_dia
            )
        
        super().save(*args, **kwargs)

    def get_clave_cliente_desencriptada(self):
        """Desencripta la clave del cliente"""
        if not self.clave_cliente:
            return ""
        
        try:
            key = get_encryption_key()
            fernet = Fernet(key)
            return fernet.decrypt(self.clave_cliente.encode()).decode()
        except:
            return "Error al desencriptar"

    def set_clave_cliente_encriptada(self, valor):
        """Encripta la clave del cliente"""
        if not valor:
            self.clave_cliente = ""
            return
        
        try:
            key = get_encryption_key()
            fernet = Fernet(key)
            self.clave_cliente = fernet.encrypt(valor.encode()).decode()
        except:
            self.clave_cliente = valor

    @property
    def dias_restantes(self):
        """Calcula los días restantes hasta el vencimiento"""
        from datetime import date
        hoy = date.today()
        if self.fecha_vencimiento and self.fecha_vencimiento >= hoy:
            return (self.fecha_vencimiento - hoy).days
        return 0

    @property
    def es_urgente(self):
        """Determina si el plazo es urgente (menos de 3 días)"""
        return self.dias_restantes <= 3 and self.dias_restantes > 0

    def clean(self):
        """Validaciones del modelo"""
        if self.fecha_inicio and self.fecha_vencimiento:
            if self.fecha_vencimiento <= self.fecha_inicio:
                raise ValidationError("La fecha de vencimiento debe ser posterior a la fecha de inicio")