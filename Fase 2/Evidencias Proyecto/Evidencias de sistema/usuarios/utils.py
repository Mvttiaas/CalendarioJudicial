"""
Utilidades para la gestión de usuarios y licencias judiciales.
"""
import re
from datetime import date, datetime
from typing import Optional, Dict, Any


def validar_licencia_judicial(numero_licencia: str, tipo_usuario: str) -> Dict[str, Any]:
    """
    Valida una licencia judicial chilena.
    
    Args:
        numero_licencia: Número de licencia a validar
        tipo_usuario: Tipo de usuario (abogado, juez, etc.)
    
    Returns:
        Dict con información de validación
    """
    if not numero_licencia:
        return {
            'valida': False,
            'error': 'Número de licencia requerido',
            'tipo_licencia': None,
            'estado': None
        }
    
    # Limpiar el número de licencia
    numero_limpio = re.sub(r'[^0-9]', '', numero_licencia)
    
    if not numero_limpio:
        return {
            'valida': False,
            'error': 'Formato de licencia inválido',
            'tipo_licencia': None,
            'estado': None
        }
    
    # Validar formato según tipo de usuario
    if tipo_usuario == 'abogado':
        return _validar_licencia_abogado(numero_limpio)
    elif tipo_usuario == 'juez':
        return _validar_licencia_juez(numero_limpio)
    elif tipo_usuario == 'asistente':
        return _validar_licencia_asistente(numero_limpio)
    else:
        return {
            'valida': True,
            'error': None,
            'tipo_licencia': 'general',
            'estado': 'activa'
        }


def _validar_licencia_abogado(numero: str) -> Dict[str, Any]:
    """
    Valida licencia de abogado.
    
    Args:
        numero: Número de licencia limpio
    
    Returns:
        Dict con información de validación
    """
    # Las licencias de abogado en Chile suelen tener 6-8 dígitos
    if len(numero) < 6 or len(numero) > 8:
        return {
            'valida': False,
            'error': 'Formato de licencia de abogado inválido (6-8 dígitos)',
            'tipo_licencia': 'abogado',
            'estado': None
        }
    
    # Verificar que no sea un número obviamente falso
    if numero.startswith('000') or numero in ['123456', '1234567', '12345678', '123456789']:
        return {
            'valida': False,
            'error': 'Número de licencia no válido',
            'tipo_licencia': 'abogado',
            'estado': None
        }
    
    return {
        'valida': True,
        'error': None,
        'tipo_licencia': 'abogado',
        'estado': 'activa'
    }


def _validar_licencia_juez(numero: str) -> Dict[str, Any]:
    """
    Valida licencia de juez.
    
    Args:
        numero: Número de licencia limpio
    
    Returns:
        Dict con información de validación
    """
    # Las licencias de juez suelen tener un formato específico
    if len(numero) < 4 or len(numero) > 6:
        return {
            'valida': False,
            'error': 'Formato de licencia de juez inválido (4-6 dígitos)',
            'tipo_licencia': 'juez',
            'estado': None
        }
    
    return {
        'valida': True,
        'error': None,
        'tipo_licencia': 'juez',
        'estado': 'activa'
    }


def _validar_licencia_asistente(numero: str) -> Dict[str, Any]:
    """
    Valida licencia de asistente legal.
    
    Args:
        numero: Número de licencia limpio
    
    Returns:
        Dict con información de validación
    """
    # Las licencias de asistente pueden tener formato más flexible
    if len(numero) < 4 or len(numero) > 10:
        return {
            'valida': False,
            'error': 'Formato de licencia de asistente inválido (4-10 dígitos)',
            'tipo_licencia': 'asistente',
            'estado': None
        }
    
    return {
        'valida': True,
        'error': None,
        'tipo_licencia': 'asistente',
        'estado': 'activa'
    }


def formatear_licencia(numero: str, tipo_usuario: str) -> str:
    """
    Formatea un número de licencia según el tipo de usuario.
    
    Args:
        numero: Número de licencia
        tipo_usuario: Tipo de usuario
    
    Returns:
        Número de licencia formateado
    """
    if not numero:
        return ''
    
    numero_limpio = re.sub(r'[^0-9]', '', numero)
    
    if tipo_usuario == 'abogado':
        # Formato: 123456-7
        if len(numero_limpio) >= 6:
            return f"{numero_limpio[:6]}-{numero_limpio[6:8] if len(numero_limpio) > 6 else ''}"
    elif tipo_usuario == 'juez':
        # Formato: JUEZ-12345
        return f"JUEZ-{numero_limpio}"
    elif tipo_usuario == 'asistente':
        # Formato: LICENCIA123
        return f"LICENCIA{numero_limpio}"
    
    return numero_limpio


def verificar_estado_licencia(numero_licencia: str, tipo_usuario: str) -> Dict[str, Any]:
    """
    Verifica el estado de una licencia judicial.
    
    Args:
        numero_licencia: Número de licencia
        tipo_usuario: Tipo de usuario
    
    Returns:
        Dict con información del estado
    """
    # En un sistema real, esto consultaría una base de datos externa
    # Por ahora, simulamos la verificación
    
    validacion = validar_licencia_judicial(numero_licencia, tipo_usuario)
    
    if not validacion['valida']:
        return {
            'estado': 'invalida',
            'mensaje': validacion['error'],
            'fecha_vencimiento': None,
            'sanciones': []
        }
    
    # Simular diferentes estados
    numero_limpio = re.sub(r'[^0-9]', '', numero_licencia)
    ultimo_digito = int(numero_limpio[-1]) if numero_limpio else 0
    
    if ultimo_digito == 0:
        return {
            'estado': 'suspendida',
            'mensaje': 'Licencia suspendida temporalmente',
            'fecha_vencimiento': None,
            'sanciones': ['Suspensión temporal']
        }
    elif ultimo_digito == 1:
        return {
            'estado': 'vencida',
            'mensaje': 'Licencia vencida',
            'fecha_vencimiento': date(2023, 12, 31),
            'sanciones': []
        }
    else:
        return {
            'estado': 'activa',
            'mensaje': 'Licencia activa y vigente',
            'fecha_vencimiento': date(2025, 12, 31),
            'sanciones': []
        }


def obtener_especialidades_por_tipo(tipo_usuario: str) -> list:
    """
    Obtiene las especialidades disponibles según el tipo de usuario.
    
    Args:
        tipo_usuario: Tipo de usuario
    
    Returns:
        Lista de especialidades disponibles
    """
    especialidades_generales = [
        ('civil', 'Derecho Civil'),
        ('penal', 'Derecho Penal'),
        ('laboral', 'Derecho Laboral'),
        ('familia', 'Derecho de Familia'),
        ('comercial', 'Derecho Comercial'),
        ('administrativo', 'Derecho Administrativo'),
        ('constitucional', 'Derecho Constitucional'),
        ('otro', 'Otra Especialidad'),
    ]
    
    if tipo_usuario == 'juez':
        # Los jueces pueden tener especialidades más específicas
        especialidades_generales.extend([
            ('civil_familia', 'Civil y Familia'),
            ('penal_garantias', 'Penal y Garantías'),
            ('laboral_previsional', 'Laboral y Previsional'),
            ('administrativo_tributario', 'Administrativo y Tributario'),
        ])
    
    return especialidades_generales


def validar_permisos_usuario(usuario, accion: str) -> bool:
    """
    Valida si un usuario tiene permisos para realizar una acción.
    
    Args:
        usuario: Instancia del usuario
        accion: Acción a realizar
    
    Returns:
        True si tiene permisos, False en caso contrario
    """
    if not usuario or not usuario.is_authenticated:
        return False
    
    # Verificar estado de la licencia
    estado_licencia = verificar_estado_licencia(usuario.numero_licencia, usuario.tipo_usuario)
    
    if estado_licencia['estado'] != 'activa':
        return False
    
    # Definir permisos por tipo de usuario
    permisos = {
        'abogado': [
            'crear_plazo', 'editar_plazo', 'eliminar_plazo', 'ver_plazos',
            'exportar_pdf', 'exportar_ics', 'ver_calendario'
        ],
        'juez': [
            'crear_plazo', 'editar_plazo', 'eliminar_plazo', 'ver_plazos',
            'exportar_pdf', 'exportar_ics', 'ver_calendario', 'ver_todos_plazos',
            'administrar_usuarios'
        ],
        'asistente': [
            'crear_plazo', 'editar_plazo', 'ver_plazos', 'exportar_pdf',
            'exportar_ics', 'ver_calendario'
        ],
        'administrador': [
            'crear_plazo', 'editar_plazo', 'eliminar_plazo', 'ver_plazos',
            'exportar_pdf', 'exportar_ics', 'ver_calendario', 'ver_todos_plazos',
            'administrar_usuarios', 'administrar_sistema'
        ]
    }
    
    return accion in permisos.get(usuario.tipo_usuario, [])


def obtener_estadisticas_usuario(usuario) -> Dict[str, Any]:
    """
    Obtiene estadísticas del usuario.
    
    Args:
        usuario: Instancia del usuario
    
    Returns:
        Dict con estadísticas
    """
    from plazos.models import PlazoJudicial
    
    if not usuario or not usuario.is_authenticated:
        return {}
    
    plazos = PlazoJudicial.objects.filter(usuario=usuario)
    
    return {
        'total_plazos': plazos.count(),
        'plazos_activos': plazos.filter(estado='corriendo').count(),
        'plazos_vencidos': plazos.filter(estado='vencido').count(),
        'plazos_suspendidos': plazos.filter(estado='suspendido').count(),
        'plazos_urgentes': plazos.filter(
            fecha_vencimiento__lte=date.today() + timedelta(days=3),
            estado='corriendo'
        ).count(),
        'tipo_usuario': usuario.tipo_usuario,
        'especialidad': usuario.especialidad,
        'fecha_registro': usuario.date_joined,
        'ultima_actividad': usuario.last_login
    }
