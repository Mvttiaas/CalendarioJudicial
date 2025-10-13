from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class Usuario(AbstractUser):
    """
    Modelo de usuario personalizado para abogados y jueces.
    Extiende el modelo User de Django con campos adicionales.
    """
    
    TIPO_USUARIO_CHOICES = [
        ('abogado', 'Abogado'),
        ('juez', 'Juez'),
        ('asistente', 'Asistente Legal'),
        ('administrador', 'Administrador'),
    ]
    
    ESPECIALIDAD_CHOICES = [
        ('civil', 'Derecho Civil'),
        ('penal', 'Derecho Penal'),
        ('laboral', 'Derecho Laboral'),
        ('familia', 'Derecho de Familia'),
        ('comercial', 'Derecho Comercial'),
        ('administrativo', 'Derecho Administrativo'),
        ('constitucional', 'Derecho Constitucional'),
        ('otro', 'Otra Especialidad'),
    ]
    
    # Campos adicionales
    tipo_usuario = models.CharField(
        max_length=20,
        choices=TIPO_USUARIO_CHOICES,
        default='abogado',
        verbose_name="Tipo de Usuario"
    )
    
    especialidad = models.CharField(
        max_length=20,
        choices=ESPECIALIDAD_CHOICES,
        default='civil',
        verbose_name="Especialidad"
    )
    
    rut = models.CharField(
        max_length=12,
        unique=True,
        verbose_name="RUT",
        help_text="Formato: 12.345.678-9"
    )
    
    telefono = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name="Teléfono"
    )
    
    
    numero_licencia = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Número de Licencia",
        help_text="Número de licencia profesional (formato: 123456-7 para abogados)",
        validators=[RegexValidator(
            regex=r'^[0-9\-A-Za-z]+$',
            message='Formato de licencia inválido'
        )]
    )
    
    fecha_nacimiento = models.DateField(
        blank=True,
        null=True,
        verbose_name="Fecha de Nacimiento"
    )
    
    biografia = models.TextField(
        blank=True,
        null=True,
        verbose_name="Biografía"
    )
    
    foto_perfil = models.ImageField(
        upload_to='perfiles/',
        blank=True,
        null=True,
        verbose_name="Foto de Perfil"
    )
    
    es_activo = models.BooleanField(
        default=True,
        verbose_name="Usuario Activo"
    )
    
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Creación"
    )
    
    fecha_modificacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de Modificación"
    )
    
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_tipo_usuario_display()})"
    
    def get_nombre_completo(self):
        """Retorna el nombre completo del usuario"""
        return f"{self.first_name} {self.last_name}".strip() or self.username
    
    def get_iniciales(self):
        """Retorna las iniciales del usuario"""
        iniciales = ""
        if self.first_name:
            iniciales += self.first_name[0].upper()
        if self.last_name:
            iniciales += self.last_name[0].upper()
        return iniciales or self.username[0].upper()
    
    def es_abogado(self):
        """Verifica si el usuario es abogado"""
        return self.tipo_usuario == 'abogado'
    
    def es_juez(self):
        """Verifica si el usuario es juez"""
        return self.tipo_usuario == 'juez'
    
    def es_asistente(self):
        """Verifica si el usuario es asistente legal"""
        return self.tipo_usuario == 'asistente'
    
    def es_administrador(self):
        """Verifica si el usuario es administrador"""
        return self.tipo_usuario == 'administrador' or self.is_superuser


class PerfilUsuario(models.Model):
    """
    Perfil extendido para usuarios con configuraciones adicionales.
    """
    
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='perfil'
    )
    
    tema_preferido = models.CharField(
        max_length=10,
        choices=[
            ('light', 'Claro'),
            ('dark', 'Oscuro'),
            ('auto', 'Automático'),
        ],
        default='light',
        verbose_name="Tema Preferido"
    )
    
    notificaciones_email = models.BooleanField(
        default=True,
        verbose_name="Notificaciones por Email"
    )
    
    notificaciones_push = models.BooleanField(
        default=True,
        verbose_name="Notificaciones Push"
    )
    
    recordar_filtros = models.BooleanField(
        default=True,
        verbose_name="Recordar Filtros"
    )
    
    plazos_por_pagina = models.PositiveIntegerField(
        default=20,
        verbose_name="Plazos por Página"
    )
    
    idioma = models.CharField(
        max_length=5,
        choices=[
            ('es', 'Español'),
            ('en', 'English'),
        ],
        default='es',
        verbose_name="Idioma"
    )
    
    zona_horaria = models.CharField(
        max_length=50,
        default='America/Santiago',
        verbose_name="Zona Horaria"
    )
    
    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuario"
    
    def __str__(self):
        return f"Perfil de {self.usuario.get_nombre_completo()}"

