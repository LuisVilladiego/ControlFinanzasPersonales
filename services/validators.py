"""
Servicio de validación de datos.

Proporciona funciones para validar datos de entrada en toda la aplicación.
"""
from datetime import datetime, date
from decimal import Decimal, InvalidOperation
from typing import Optional, Tuple


class ValidationError(Exception):
    """Excepción personalizada para errores de validación."""
    pass


def validate_email(email: str) -> Tuple[bool, Optional[str]]:
    """
    Valida un email.
    
    Args:
        email: Email a validar
        
    Returns:
        Tupla (es_valido, mensaje_error)
    """
    if not email:
        return False, "El email es requerido"
    
    if '@' not in email or '.' not in email.split('@')[1]:
        return False, "El formato del email no es válido"
    
    if len(email) > 120:
        return False, "El email es demasiado largo (máximo 120 caracteres)"
    
    return True, None


def validate_password(password: str, min_length: int = 6) -> Tuple[bool, Optional[str]]:
    """
    Valida una contraseña.
    
    Args:
        password: Contraseña a validar
        min_length: Longitud mínima requerida
        
    Returns:
        Tupla (es_valido, mensaje_error)
    """
    if not password:
        return False, "La contraseña es requerida"
    
    if len(password) < min_length:
        return False, f"La contraseña debe tener al menos {min_length} caracteres"
    
    return True, None


def validate_monto(monto: str) -> Tuple[bool, Optional[str], Optional[Decimal]]:
    """
    Valida un monto monetario.
    
    Args:
        monto: Monto a validar (string o número)
        
    Returns:
        Tupla (es_valido, mensaje_error, monto_decimal)
    """
    if not monto:
        return False, "El monto es requerido", None
    
    try:
        monto_decimal = Decimal(str(monto))
        
        if monto_decimal < 0:
            return False, "El monto no puede ser negativo", None
        
        if monto_decimal > Decimal('999999999.99'):
            return False, "El monto es demasiado grande", None
        
        return True, None, monto_decimal
    except (InvalidOperation, ValueError):
        return False, "El monto debe ser un número válido", None


def validate_fecha(fecha_str: str, formato: str = '%Y-%m-%d') -> Tuple[bool, Optional[str], Optional[date]]:
    """
    Valida una fecha.
    
    Args:
        fecha_str: Fecha en formato string
        formato: Formato esperado de la fecha
        
    Returns:
        Tupla (es_valido, mensaje_error, fecha_date)
    """
    if not fecha_str:
        return False, "La fecha es requerida", None
    
    try:
        fecha = datetime.strptime(fecha_str, formato).date()
        
        if fecha > date.today() + date.resolution * 365 * 10:  # No más de 10 años en el futuro
            return False, "La fecha no puede ser más de 10 años en el futuro", None
        
        return True, None, fecha
    except ValueError:
        return False, f"La fecha debe estar en formato {formato}", None


def validate_fecha_limite(fecha_limite: date, fecha_inicio: Optional[date] = None) -> Tuple[bool, Optional[str]]:
    """
    Valida que una fecha límite sea posterior a una fecha de inicio.
    
    Args:
        fecha_limite: Fecha límite a validar
        fecha_inicio: Fecha de inicio (opcional)
        
    Returns:
        Tupla (es_valido, mensaje_error)
    """
    if fecha_inicio and fecha_limite < fecha_inicio:
        return False, "La fecha límite debe ser posterior a la fecha de inicio"
    
    if fecha_limite < date.today():
        return False, "La fecha límite no puede ser en el pasado"
    
    return True, None


def validate_texto(texto: str, campo: str, max_length: int = 255, required: bool = True) -> Tuple[bool, Optional[str]]:
    """
    Valida un texto.
    
    Args:
        texto: Texto a validar
        campo: Nombre del campo (para mensajes de error)
        max_length: Longitud máxima
        required: Si el campo es requerido
        
    Returns:
        Tupla (es_valido, mensaje_error)
    """
    if required and not texto:
        return False, f"{campo} es requerido"
    
    if texto and len(texto) > max_length:
        return False, f"{campo} es demasiado largo (máximo {max_length} caracteres)"
    
    return True, None


def validate_categoria(categoria: str, tipo: str = 'egreso') -> Tuple[bool, Optional[str]]:
    """
    Valida una categoría.
    
    Args:
        categoria: Categoría a validar
        tipo: Tipo de categoría ('ingreso' o 'egreso')
        
    Returns:
        Tupla (es_valido, mensaje_error)
    """
    categorias_validas = {
        'ingreso': ['Salario', 'Freelance', 'Inversiones', 'Ventas', 'Otros'],
        'egreso': ['Alimentación', 'Transporte', 'Vivienda', 'Servicios', 
                   'Entretenimiento', 'Salud', 'Educación', 'Ropa', 'Otros']
    }
    
    if not categoria:
        return False, "La categoría es requerida"
    
    if categoria not in categorias_validas.get(tipo, []):
        return False, f"La categoría '{categoria}' no es válida para {tipo}"
    
    return True, None


def validate_frecuencia(frecuencia: str) -> Tuple[bool, Optional[str]]:
    """
    Valida una frecuencia de ahorro.
    
    Args:
        frecuencia: Frecuencia a validar
        
    Returns:
        Tupla (es_valido, mensaje_error)
    """
    frecuencias_validas = ['diaria', 'semanal', 'mensual', 'anual']
    
    if not frecuencia:
        return False, "La frecuencia es requerida"
    
    if frecuencia not in frecuencias_validas:
        return False, f"La frecuencia '{frecuencia}' no es válida. Debe ser una de: {', '.join(frecuencias_validas)}"
    
    return True, None


