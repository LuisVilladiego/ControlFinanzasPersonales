"""
Pruebas para el servicio de transacciones.
"""
import pytest
from datetime import date
from services.transacciones_service import TransaccionesService
from services.validators import ValidationError
from models import Ingreso, Egreso


class TestTransaccionesService:
    """Pruebas para el servicio de transacciones."""
    
    def test_crear_ingreso_valido(self, app, usuario_test):
        """Prueba crear un ingreso válido."""
        with app.app_context():
            ingreso = TransaccionesService.crear_ingreso(
                usuario_id=usuario_test.id,
                monto='1000.00',
                descripcion='Salario',
                categoria='Salario',
                fecha='2024-01-15'
            )
            
            assert ingreso.id is not None
            assert float(ingreso.monto) == 1000.00
            assert ingreso.descripcion == 'Salario'
            assert ingreso.categoria == 'Salario'
    
    def test_crear_ingreso_monto_invalido(self, app, usuario_test):
        """Prueba que crear un ingreso con monto inválido falle."""
        with app.app_context():
            with pytest.raises(ValidationError):
                TransaccionesService.crear_ingreso(
                    usuario_id=usuario_test.id,
                    monto='-100',
                    descripcion='Salario',
                    categoria='Salario',
                    fecha='2024-01-15'
                )
    
    def test_crear_egreso_valido(self, app, usuario_test):
        """Prueba crear un egreso válido."""
        with app.app_context():
            egreso = TransaccionesService.crear_egreso(
                usuario_id=usuario_test.id,
                monto='50.00',
                descripcion='Supermercado',
                categoria='Alimentación',
                fecha='2024-01-15'
            )
            
            assert egreso.id is not None
            assert float(egreso.monto) == 50.00
            assert egreso.descripcion == 'Supermercado'
    
    def test_actualizar_ingreso(self, app, usuario_test):
        """Prueba actualizar un ingreso."""
        with app.app_context():
            ingreso = TransaccionesService.crear_ingreso(
                usuario_id=usuario_test.id,
                monto='1000.00',
                descripcion='Salario',
                categoria='Salario',
                fecha='2024-01-15'
            )
            
            ingreso_actualizado = TransaccionesService.actualizar_ingreso(
                ingreso,
                monto='1200.00',
                descripcion='Salario actualizado'
            )
            
            assert float(ingreso_actualizado.monto) == 1200.00
            assert ingreso_actualizado.descripcion == 'Salario actualizado'
    
    def test_eliminar_ingreso(self, app, usuario_test):
        """Prueba eliminar un ingreso."""
        with app.app_context():
            ingreso = TransaccionesService.crear_ingreso(
                usuario_id=usuario_test.id,
                monto='1000.00',
                descripcion='Salario',
                categoria='Salario',
                fecha='2024-01-15'
            )
            
            ingreso_id = ingreso.id
            TransaccionesService.eliminar_ingreso(ingreso)
            
            # Verificar que fue eliminado
            ingreso_eliminado = Ingreso.query.get(ingreso_id)
            assert ingreso_eliminado is None


