"""
Utilidades para el cálculo de plazos judiciales en Chile.
Incluye lógica para días hábiles, feriados y cálculos de vencimiento.
"""

from datetime import date, timedelta
import holidays
from typing import Optional


def es_dia_habil(fecha: date, pais: str = 'Chile') -> bool:
    """
    Verifica si una fecha es día hábil en Chile.
    
    Args:
        fecha: Fecha a verificar
        pais: País para verificar feriados (por defecto 'Chile')
    
    Returns:
        True si es día hábil, False en caso contrario
    """
    # Verificar si es fin de semana (sábado = 5, domingo = 6)
    if fecha.weekday() >= 5:
        return False
    
    # Verificar si es feriado
    chile_holidays = holidays.Chile()
    return fecha not in chile_holidays


def obtener_feriados_chile(ano: int) -> list:
    """
    Obtiene la lista de feriados para un año específico en Chile.
    
    Args:
        ano: Año para obtener los feriados
    
    Returns:
        Lista de fechas de feriados
    """
    chile_holidays = holidays.Chile()
    return [fecha for fecha in chile_holidays.keys() if fecha.year == ano]


def calcular_fecha_vencimiento(
    fecha_inicio: date,
    dias_plazo: int,
    tipo_dia: str
) -> Optional[date]:
    """
    Calcula la fecha de vencimiento de un plazo judicial.
    
    Args:
        fecha_inicio: Fecha de inicio del plazo
        dias_plazo: Número de días del plazo
        tipo_dia: Tipo de día ('habil' o 'corrido')
    
    Returns:
        Fecha de vencimiento calculada o None si hay error
    
    Nota:
        - El plazo comienza al día siguiente de la fecha_inicio
        - Para días hábiles, excluye fines de semana y feriados chilenos
        - Para días corridos, incluye todos los días
    """
    if not fecha_inicio or dias_plazo <= 0:
        return None
    
    # El plazo comienza al día siguiente de la fecha_inicio
    fecha_actual = fecha_inicio + timedelta(days=1)
    dias_contados = 0
    
    if tipo_dia == 'corrido':
        # Para días corridos, simplemente sumar los días
        return fecha_actual + timedelta(days=dias_plazo - 1)
    
    elif tipo_dia == 'habil':
        # Para días hábiles, contar solo días hábiles
        while dias_contados < dias_plazo:
            if es_dia_habil(fecha_actual):
                dias_contados += 1
            fecha_actual += timedelta(days=1)
        
        # Retroceder un día porque el bucle avanza uno de más
        return fecha_actual - timedelta(days=1)
    
    return None


def calcular_dias_habiles_entre_fechas(fecha_inicio: date, fecha_fin: date) -> int:
    """
    Calcula el número de días hábiles entre dos fechas.
    
    Args:
        fecha_inicio: Fecha de inicio
        fecha_fin: Fecha de fin
    
    Returns:
        Número de días hábiles entre las fechas
    """
    if fecha_inicio > fecha_fin:
        return 0
    
    dias_habiles = 0
    fecha_actual = fecha_inicio
    
    while fecha_actual <= fecha_fin:
        if es_dia_habil(fecha_actual):
            dias_habiles += 1
        fecha_actual += timedelta(days=1)
    
    return dias_habiles


def obtener_proximo_dia_habil(fecha: date) -> date:
    """
    Obtiene el próximo día hábil a partir de una fecha.
    
    Args:
        fecha: Fecha de referencia
    
    Returns:
        Próximo día hábil
    """
    fecha_actual = fecha + timedelta(days=1)
    
    while not es_dia_habil(fecha_actual):
        fecha_actual += timedelta(days=1)
    
    return fecha_actual


def es_fecha_vencimiento_valida(fecha_vencimiento: date, tipo_dia: str) -> bool:
    """
    Verifica si una fecha de vencimiento es válida según el tipo de día.
    
    Args:
        fecha_vencimiento: Fecha de vencimiento a verificar
        tipo_dia: Tipo de día ('habil' o 'corrido')
    
    Returns:
        True si la fecha es válida, False en caso contrario
    """
    if tipo_dia == 'habil':
        return es_dia_habil(fecha_vencimiento)
    elif tipo_dia == 'corrido':
        return True
    
    return False


def obtener_estado_plazo(fecha_vencimiento: date, estado_actual: str) -> str:
    """
    Determina el estado de un plazo basado en su fecha de vencimiento.
    
    Args:
        fecha_vencimiento: Fecha de vencimiento del plazo
        estado_actual: Estado actual del plazo
    
    Returns:
        Estado actualizado del plazo
    """
    if estado_actual in ['suspendido', 'esperando_proveido']:
        return estado_actual
    
    fecha_actual = date.today()
    
    if fecha_actual > fecha_vencimiento:
        return 'vencido'
    elif fecha_actual == fecha_vencimiento:
        return 'corriendo'
    else:
        return 'corriendo'


def formatear_fecha_chilena(fecha: date) -> str:
    """
    Formatea una fecha en formato chileno (dd/mm/yyyy).
    
    Args:
        fecha: Fecha a formatear
    
    Returns:
        Fecha formateada como string
    """
    return fecha.strftime('%d/%m/%Y')


def obtener_nombre_dia_semana(fecha: date) -> str:
    """
    Obtiene el nombre del día de la semana en español.
    
    Args:
        fecha: Fecha para obtener el día
    
    Returns:
        Nombre del día de la semana en español
    """
    dias_semana = [
        'Lunes', 'Martes', 'Miércoles', 'Jueves', 
        'Viernes', 'Sábado', 'Domingo'
    ]
    return dias_semana[fecha.weekday()]


def es_plazo_urgente(fecha_vencimiento: date, dias_anticipacion: int = 3) -> bool:
    """
    Verifica si un plazo está próximo a vencer (urgente).
    
    Args:
        fecha_vencimiento: Fecha de vencimiento del plazo
        dias_anticipacion: Días de anticipación para considerar urgente
    
    Returns:
        True si el plazo es urgente, False en caso contrario
    """
    fecha_actual = date.today()
    dias_restantes = (fecha_vencimiento - fecha_actual).days
    
    return 0 <= dias_restantes <= dias_anticipacion


def validar_rut_chileno(rut: str) -> bool:
    """
    Valida un RUT chileno verificando su formato y dígito verificador.
    
    Args:
        rut: RUT a validar (puede incluir puntos y guión)
    
    Returns:
        True si el RUT es válido, False en caso contrario
    """
    if not rut:
        return False
    
    # Limpiar el RUT: quitar puntos, espacios y convertir a mayúscula
    rut_limpio = rut.replace('.', '').replace(' ', '').replace('-', '').upper()
    
    # Verificar que tenga al menos 8 caracteres (7 dígitos + 1 verificador)
    if len(rut_limpio) < 8 or len(rut_limpio) > 9:
        return False
    
    # Separar el número del dígito verificador
    numero = rut_limpio[:-1]
    verificador = rut_limpio[-1]
    
    # Verificar que el número solo contenga dígitos
    if not numero.isdigit():
        return False
    
    # Verificar que el verificador sea un dígito o K
    if verificador not in '0123456789K':
        return False
    
    # Calcular el dígito verificador correcto
    verificador_calculado = calcular_digito_verificador(numero)
    
    # Comparar con el verificador proporcionado
    return verificador == verificador_calculado


def calcular_digito_verificador(numero: str) -> str:
    """
    Calcula el dígito verificador de un RUT chileno.
    
    Args:
        numero: Número del RUT sin dígito verificador
    
    Returns:
        Dígito verificador calculado
    """
    # Invertir el número para el cálculo
    numero_invertido = numero[::-1]
    
    # Factores de multiplicación
    factores = [2, 3, 4, 5, 6, 7]
    
    # Calcular la suma
    suma = 0
    for i, digito in enumerate(numero_invertido):
        factor = factores[i % len(factores)]
        suma += int(digito) * factor
    
    # Calcular el resto
    resto = suma % 11
    
    # Determinar el dígito verificador
    if resto == 0:
        return '0'
    elif resto == 1:
        return 'K'
    else:
        return str(11 - resto)


def formatear_rut_chileno(rut: str) -> str:
    """
    Formatea un RUT chileno con puntos y guión.
    
    Args:
        rut: RUT sin formato
    
    Returns:
        RUT formateado (ej: 12.345.678-9)
    """
    if not rut:
        return ''
    
    # Limpiar el RUT
    rut_limpio = rut.replace('.', '').replace(' ', '').replace('-', '').upper()
    
    if len(rut_limpio) < 8:
        return rut
    
    # Separar número y verificador
    numero = rut_limpio[:-1]
    verificador = rut_limpio[-1]
    
    # Agregar puntos cada 3 dígitos desde la derecha
    numero_formateado = ''
    for i, digito in enumerate(numero[::-1]):
        if i > 0 and i % 3 == 0:
            numero_formateado = '.' + numero_formateado
        numero_formateado = digito + numero_formateado
    
    return f"{numero_formateado}-{verificador}"


def es_rut_valido_para_causa(rut: str) -> bool:
    """
    Verifica si un RUT es válido para ser usado como RUT de causa.
    Incluye validaciones adicionales específicas para causas judiciales.
    
    Args:
        rut: RUT a validar
    
    Returns:
        True si el RUT es válido para causa, False en caso contrario
    """
    # Validar formato y dígito verificador
    if not validar_rut_chileno(rut):
        return False
    
    # Limpiar el RUT para obtener solo el número
    rut_limpio = rut.replace('.', '').replace(' ', '').replace('-', '').upper()
    numero = rut_limpio[:-1]
    
    # Verificar que el número tenga al menos 7 dígitos (RUTs válidos en Chile)
    if len(numero) < 7:
        return False
    
    # Verificar que no sea un RUT obviamente falso (como 0000000)
    if numero == '0000000' or numero.startswith('000000'):
        return False
    
    # Verificar que no sea un RUT de prueba común
    ruts_prueba = ['11111111', '12345678', '98765432', '00000001']
    if rut_limpio in ruts_prueba:
        return False
    
    return True
