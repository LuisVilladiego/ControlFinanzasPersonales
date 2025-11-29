"""
Pruebas para el módulo de validadores.
"""
import pytest
from services.validators import (
    validate_email, validate_password, validate_monto,
    validate_fecha, validate_texto, validate_categoria,
    validate_frecuencia, ValidationError
)


class TestEmailValidator:
    """Pruebas para validación de email."""
    
    def test_email_valido(self):
        """Prueba que un email válido pase la validación."""
        es_valido, error = validate_email('test@example.com')
        assert es_valido is True
        assert error is None
    
    def test_email_invalido_sin_arroba(self):
        """Prueba que un email sin @ falle."""
        es_valido, error = validate_email('testexample.com')
        assert es_valido is False
        assert error is not None
    
    def test_email_vacio(self):
        """Prueba que un email vacío falle."""
        es_valido, error = validate_email('')
        assert es_valido is False
        assert 'requerido' in error.lower()


class TestPasswordValidator:
    """Pruebas para validación de contraseña."""
    
    def test_password_valido(self):
        """Prueba que una contraseña válida pase."""
        es_valido, error = validate_password('password123')
        assert es_valido is True
        assert error is None
    
    def test_password_corto(self):
        """Prueba que una contraseña corta falle."""
        es_valido, error = validate_password('12345')
        assert es_valido is False
        assert 'al menos' in error.lower()
    
    def test_password_vacio(self):
        """Prueba que una contraseña vacía falle."""
        es_valido, error = validate_password('')
        assert es_valido is False
        assert 'requerida' in error.lower()


class TestMontoValidator:
    """Pruebas para validación de montos."""
    
    def test_monto_valido(self):
        """Prueba que un monto válido pase."""
        es_valido, error, monto = validate_monto('100.50')
        assert es_valido is True
        assert error is None
        assert float(monto) == 100.50
    
    def test_monto_negativo(self):
        """Prueba que un monto negativo falle."""
        es_valido, error, monto = validate_monto('-100')
        assert es_valido is False
        assert 'negativo' in error.lower()
    
    def test_monto_invalido(self):
        """Prueba que un monto inválido falle."""
        es_valido, error, monto = validate_monto('abc')
        assert es_valido is False
        assert error is not None


class TestFechaValidator:
    """Pruebas para validación de fechas."""
    
    def test_fecha_valida(self):
        """Prueba que una fecha válida pase."""
        es_valido, error, fecha = validate_fecha('2024-01-15')
        assert es_valido is True
        assert error is None
        assert fecha is not None
    
    def test_fecha_formato_invalido(self):
        """Prueba que una fecha con formato inválido falle."""
        es_valido, error, fecha = validate_fecha('15/01/2024')
        assert es_valido is False
        assert error is not None


class TestCategoriaValidator:
    """Pruebas para validación de categorías."""
    
    def test_categoria_ingreso_valida(self):
        """Prueba que una categoría de ingreso válida pase."""
        es_valido, error = validate_categoria('Salario', 'ingreso')
        assert es_valido is True
        assert error is None
    
    def test_categoria_egreso_valida(self):
        """Prueba que una categoría de egreso válida pase."""
        es_valido, error = validate_categoria('Alimentación', 'egreso')
        assert es_valido is True
        assert error is None
    
    def test_categoria_invalida(self):
        """Prueba que una categoría inválida falle."""
        es_valido, error = validate_categoria('CategoriaInvalida', 'ingreso')
        assert es_valido is False
        assert error is not None


class TestFrecuenciaValidator:
    """Pruebas para validación de frecuencias."""
    
    def test_frecuencia_valida(self):
        """Prueba que una frecuencia válida pase."""
        es_valido, error = validate_frecuencia('mensual')
        assert es_valido is True
        assert error is None
    
    def test_frecuencia_invalida(self):
        """Prueba que una frecuencia inválida falle."""
        es_valido, error = validate_frecuencia('semanalmente')
        assert es_valido is False
        assert error is not None


