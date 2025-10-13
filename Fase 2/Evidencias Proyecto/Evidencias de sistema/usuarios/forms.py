from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import Usuario, PerfilUsuario
from .utils import validar_licencia_judicial, formatear_licencia


class FormularioRegistro(UserCreationForm):
    """
    Formulario de registro personalizado para usuarios.
    """
    
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre'
        }),
        label='Nombre'
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Apellido'
        }),
        label='Apellido'
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'correo@ejemplo.com'
        }),
        label='Correo Electrónico'
    )
    
    tipo_usuario = forms.ChoiceField(
        choices=Usuario.TIPO_USUARIO_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label='Tipo de Usuario'
    )
    
    especialidad = forms.ChoiceField(
        choices=Usuario.ESPECIALIDAD_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label='Especialidad'
    )
    
    rut = forms.CharField(
        max_length=12,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '12.345.678-9',
            'pattern': r'^\d{1,2}\.\d{3}\.\d{3}-[\dkK]$'
        }),
        label='RUT',
        help_text='Formato: 12.345.678-9'
    )
    
    telefono = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+56 9 1234 5678'
        }),
        label='Teléfono'
    )
    
    
    numero_licencia = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Número de licencia profesional'
        }),
        label='Número de Licencia'
    )
    
    
    
    class Meta:
        model = Usuario
        fields = (
            'username', 'first_name', 'last_name', 'email',
            'tipo_usuario', 'especialidad', 'rut', 'telefono',
            'numero_licencia', 'password1', 'password2'
        )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar widgets de contraseña
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Nombre de usuario'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Contraseña'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirmar contraseña'
        })
    
    def clean_rut(self):
        """Valida el RUT chileno"""
        rut = self.cleaned_data.get('rut')
        if not rut:
            return rut
        
        # Limpiar el RUT
        rut_limpio = rut.replace('.', '').replace('-', '').strip()
        
        if len(rut_limpio) < 8 or len(rut_limpio) > 9:
            raise ValidationError('RUT inválido. Debe tener entre 8 y 9 caracteres.')
        
        # Verificar que solo contenga números y K
        if not rut_limpio[:-1].isdigit() or rut_limpio[-1] not in '0123456789kK':
            raise ValidationError('RUT inválido. Solo números y K permitidos.')
        
        # Verificar dígito verificador
        if not self._validar_digito_verificador(rut_limpio):
            raise ValidationError('RUT inválido. El dígito verificador no es correcto.')
        
        # Formatear RUT correctamente
        numero = rut_limpio[:-1]
        dv = rut_limpio[-1].upper()
        if len(numero) == 8:
            rut_formateado = f"{numero[:2]}.{numero[2:5]}.{numero[5:]}-{dv}"
        else:
            rut_formateado = f"{numero[:-3]}.{numero[-3:]}-{dv}"
        
        return rut_formateado
    
    def clean_numero_licencia(self):
        """Valida el número de licencia judicial."""
        numero_licencia = self.cleaned_data.get('numero_licencia')
        tipo_usuario = self.cleaned_data.get('tipo_usuario')
        
        if numero_licencia and tipo_usuario:
            validacion = validar_licencia_judicial(numero_licencia, tipo_usuario)
            if not validacion['valida']:
                raise ValidationError(validacion['error'])
            
            # Formatear la licencia
            return formatear_licencia(numero_licencia, tipo_usuario)
        
        return numero_licencia
    
    def _validar_digito_verificador(self, rut):
        """Valida el dígito verificador del RUT"""
        if len(rut) < 2:
            return False
        
        numero = rut[:-1]
        dv = rut[-1].upper()
        
        # Calcular dígito verificador
        suma = 0
        multiplicador = 2
        
        for digito in reversed(numero):
            suma += int(digito) * multiplicador
            multiplicador = multiplicador + 1 if multiplicador < 7 else 2
        
        resto = suma % 11
        dv_calculado = 11 - resto
        
        if dv_calculado == 11:
            dv_calculado = '0'
        elif dv_calculado == 10:
            dv_calculado = 'K'
        else:
            dv_calculado = str(dv_calculado)
        
        return dv == dv_calculado
    
    def clean_email(self):
        """Valida que el email sea único"""
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise ValidationError('Este correo electrónico ya está registrado.')
        return email
    
    def save(self, commit=True):
        """Guarda el usuario y crea su perfil"""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            # Crear perfil de usuario
            PerfilUsuario.objects.create(usuario=user)
        
        return user


class FormularioLogin(AuthenticationForm):
    """
    Formulario de login personalizado.
    """
    
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Usuario o correo electrónico',
            'autofocus': True
        }),
        label='Usuario'
    )
    
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña',
            'id': 'id_password'
        }),
        label='Contraseña'
    )
    
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='Recordarme'
    )
    


class FormularioPerfil(forms.ModelForm):
    """
    Formulario para editar perfil de usuario.
    """
    
    class Meta:
        model = Usuario
        fields = [
            'username', 'first_name', 'last_name', 'email', 'tipo_usuario',
            'especialidad', 'telefono', 'numero_licencia'
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'tipo_usuario': forms.Select(attrs={'class': 'form-select'}),
            'especialidad': forms.Select(attrs={'class': 'form-select'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_licencia': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    


class FormularioConfiguracion(forms.ModelForm):
    """
    Formulario para configuraciones del perfil.
    """
    
    class Meta:
        model = PerfilUsuario
        fields = [
            'tema_preferido', 'notificaciones_email', 'notificaciones_push',
            'recordar_filtros', 'plazos_por_pagina', 'idioma'
        ]
        widgets = {
            'tema_preferido': forms.Select(attrs={'class': 'form-select'}),
            'notificaciones_email': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notificaciones_push': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'recordar_filtros': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'plazos_por_pagina': forms.NumberInput(attrs={'class': 'form-control', 'min': '5', 'max': '100'}),
            'idioma': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Establecer valores por defecto si no hay instancia
        if not self.instance.pk:
            self.fields['tema_preferido'].initial = 'light'
            self.fields['plazos_por_pagina'].initial = 20
            self.fields['idioma'].initial = 'es'
            self.fields['notificaciones_email'].initial = True
            self.fields['notificaciones_push'].initial = True
            self.fields['recordar_filtros'].initial = True

