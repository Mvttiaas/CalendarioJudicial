from django import forms
from django.core.exceptions import ValidationError
from .models import PlazoJudicial, CodigoProcedimiento
from .utils.plazos import validar_rut_chileno, es_rut_valido_para_causa, formatear_rut_chileno
from datetime import date, timedelta


class PlazoJudicialForm(forms.ModelForm):
    """
    Formulario para crear y editar plazos judiciales.
    Incluye validaciones específicas para el sistema judicial chileno.
    """
    codigo_procedimiento = forms.ModelChoiceField(
        queryset=CodigoProcedimiento.objects.filter(activo=True).order_by('codigo'),
        required=False,
        empty_label="Seleccionar código de procedimiento (opcional)",
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_codigo_procedimiento'}),
        help_text="Seleccione un código para llenar automáticamente los campos"
    )
    
    class Meta:
        model = PlazoJudicial
        fields = [
            'codigo_procedimiento', 'tipo_documento', 'procedimiento', 'dias_plazo', 'tipo_dia',
            'fecha_inicio', 'rol', 'rut_cliente', 'clave_cliente', 'estado', 'observaciones', 'documento_adjunto'
        ]
        widgets = {
            'tipo_documento': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'procedimiento': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'dias_plazo': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '365',
                'required': True
            }),
            'tipo_dia': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'fecha_inicio': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'rol': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '123456789',
                'pattern': r'^\d+$',
                'title': 'Serie de números para identificar el proceso',
                'required': True
            }),
            'rut_cliente': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '12345678-9',
                'pattern': r'^\d{1,2}\.\d{3}\.\d{3}-[\dkK]$',
                'title': 'Formato: 12345678-9 o 12.345.678-9',
                'required': True
            }),
            'clave_cliente': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Clave para identificar al cliente',
                'required': True
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Observaciones adicionales (opcional)',
                'maxlength': '200'
            }),
            'documento_adjunto': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.txt,.jpg,.jpeg,.png',
                'title': 'Formatos permitidos: PDF, DOC, DOCX, TXT, JPG, JPEG, PNG'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Establecer fecha por defecto como hoy
        if not self.instance.pk:
            self.fields['fecha_inicio'].initial = date.today()
    
    def clean_observaciones(self):
        """
        Valida la longitud de las observaciones.
        """
        observaciones = self.cleaned_data.get('observaciones')
        if observaciones and len(observaciones) > 200:
            raise ValidationError('Las observaciones no pueden exceder los 200 caracteres.')
        return observaciones
    
    def clean_rol(self):
        """
        Valida el rol (serie de números para identificar el proceso).
        """
        rol = self.cleaned_data.get('rol')
        if not rol:
            return rol
        
        # Validar que sea solo números
        if not rol.isdigit():
            raise ValidationError('El rol debe contener solo números.')
        
        # Validar longitud mínima
        if len(rol) < 3:
            raise ValidationError('El rol debe tener al menos 3 dígitos.')
        
        return rol
    
    def clean_rut_cliente(self):
        """
        Valida el RUT del cliente usando el validador mejorado.
        """
        rut = self.cleaned_data.get('rut_cliente')
        if not rut:
            return rut
        
        # Validar que sea un RUT válido para causa judicial
        if not es_rut_valido_para_causa(rut):
            raise ValidationError(
                'RUT inválido para cliente. '
                'Verifique que el RUT sea correcto y tenga un dígito verificador válido. '
                'Formato: 12.345.678-9'
            )
        
        # Formatear el RUT correctamente
        return formatear_rut_chileno(rut)
    
    
    def clean_fecha_inicio(self):
        """
        Valida que la fecha de inicio no sea futura para ciertos tipos de documentos.
        """
        fecha_inicio = self.cleaned_data.get('fecha_inicio')
        tipo_documento = self.cleaned_data.get('tipo_documento')
        
        if fecha_inicio and tipo_documento:
            # Para ciertos documentos, la fecha no puede ser muy antigua
            if fecha_inicio < date.today() - timedelta(days=365):
                raise ValidationError('La fecha de inicio no puede ser anterior a un año.')
        
        return fecha_inicio
    
    def clean_dias_plazo(self):
        """
        Valida que el número de días de plazo sea razonable.
        """
        dias_plazo = self.cleaned_data.get('dias_plazo')
        
        if dias_plazo:
            if dias_plazo > 365:
                raise ValidationError('El plazo no puede ser superior a 365 días.')
            if dias_plazo < 1:
                raise ValidationError('El plazo debe ser de al menos 1 día.')
        
        return dias_plazo
    
    def clean_documento_adjunto(self):
        """
        Valida el archivo adjunto.
        """
        archivo = self.cleaned_data.get('documento_adjunto')
        
        if archivo:
            # Validar tamaño del archivo (máximo 10MB)
            if archivo.size > 10 * 1024 * 1024:
                raise ValidationError('El archivo no puede ser mayor a 10MB.')
            
            # Validar extensión
            extensiones_permitidas = ['.pdf', '.doc', '.docx', '.txt', '.jpg', '.jpeg', '.png']
            extension = archivo.name.lower().split('.')[-1]
            if f'.{extension}' not in extensiones_permitidas:
                raise ValidationError(
                    'Formato de archivo no permitido. '
                    'Formatos válidos: PDF, DOC, DOCX, TXT, JPG, JPEG, PNG'
                )
        
        return archivo


class FiltroPlazosForm(forms.Form):
    """
    Formulario para filtrar plazos judiciales con búsqueda avanzada.
    """
    
    TIPO_DOCUMENTO_CHOICES = [('', 'Todos los tipos')] + PlazoJudicial.TIPOS_DOCUMENTO
    PROCEDIMIENTO_CHOICES = [('', 'Todos los procedimientos')] + PlazoJudicial.TIPOS_PROCEDIMIENTO
    ESTADO_CHOICES = [('', 'Todos los estados')] + PlazoJudicial.ESTADOS
    
    # Búsqueda general
    busqueda = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por RUT, clave de cliente o observaciones...',
            'id': 'busqueda-input',
            'autocomplete': 'off',
            'data-toggle': 'tooltip',
            'title': 'Busca en RUT, clave de cliente, observaciones y más...'
        }),
        label='Búsqueda General'
    )
    
    # Filtros básicos
    tipo_documento = forms.ChoiceField(
        choices=TIPO_DOCUMENTO_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    procedimiento = forms.ChoiceField(
        choices=PROCEDIMIENTO_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    estado = forms.ChoiceField(
        choices=ESTADO_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    # Filtros de fecha
    fecha_desde = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    fecha_hasta = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    # Búsqueda específica
    rol = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por rol específico...',
            'id': 'rol-input'
        }),
        label='Rol'
    )
    
    rut_cliente = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por RUT de cliente...',
            'id': 'rut-cliente-input'
        }),
        label='RUT de Cliente'
    )
    
    clave_cliente = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por clave de cliente...',
            'id': 'clave-input'
        }),
        label='Clave de Cliente'
    )
    
    # Filtros especiales
    solo_urgentes = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    solo_vencidos = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    # Búsqueda avanzada
    busqueda_exacta = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Búsqueda exacta'
    )
    
    incluir_observaciones = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Incluir observaciones',
        initial=True
    )
    
    # Ordenamiento
    ORDEN_CHOICES = [
        ('fecha_vencimiento', 'Fecha de Vencimiento'),
        ('fecha_inicio', 'Fecha de Inicio'),
        ('tipo_documento', 'Tipo de Documento'),
        ('estado', 'Estado'),
        ('rol', 'Rol'),
        ('rut_cliente', 'RUT de Cliente'),
    ]
    
    ordenar_por = forms.ChoiceField(
        choices=ORDEN_CHOICES,
        required=False,
        initial='fecha_vencimiento',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    ASCENDENTE_CHOICES = [
        ('asc', 'Ascendente'),
        ('desc', 'Descendente'),
    ]
    
    direccion_orden = forms.ChoiceField(
        choices=ASCENDENTE_CHOICES,
        required=False,
        initial='asc',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
