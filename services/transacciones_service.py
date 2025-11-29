"""
Servicio de transacciones.

Contiene la lógica de negocio para ingresos y egresos.
"""
from typing import Optional, Dict, Any
from datetime import date
from decimal import Decimal
from database import db
from models import Ingreso, Egreso
from services.validators import (
    validate_monto, validate_fecha, validate_texto, 
    validate_categoria, ValidationError
)


class TransaccionesService:
    """Servicio para gestionar transacciones financieras."""
    
    @staticmethod
    def crear_ingreso(usuario_id: int, monto: str, descripcion: str, 
                     categoria: str, fecha: str) -> Ingreso:
        """
        Crea un nuevo ingreso.
        
        Args:
            usuario_id: ID del usuario
            monto: Monto del ingreso
            descripcion: Descripción del ingreso
            categoria: Categoría del ingreso
            fecha: Fecha del ingreso (formato YYYY-MM-DD)
            
        Returns:
            Ingreso creado
            
        Raises:
            ValidationError: Si los datos no son válidos
        """
        # Validar datos
        es_valido, error, monto_decimal = validate_monto(monto)
        if not es_valido:
            raise ValidationError(error)
        
        es_valido, error, fecha_date = validate_fecha(fecha)
        if not es_valido:
            raise ValidationError(error)
        
        es_valido, error = validate_texto(descripcion, "Descripción", max_length=255)
        if not es_valido:
            raise ValidationError(error)
        
        es_valido, error = validate_categoria(categoria, 'ingreso')
        if not es_valido:
            raise ValidationError(error)
        
        # Crear ingreso
        ingreso = Ingreso(
            usuario_id=usuario_id,
            monto=monto_decimal,
            descripcion=descripcion,
            categoria=categoria,
            fecha=fecha_date
        )
        
        db.session.add(ingreso)
        db.session.commit()
        
        return ingreso
    
    @staticmethod
    def actualizar_ingreso(ingreso: Ingreso, monto: Optional[str] = None,
                          descripcion: Optional[str] = None,
                          categoria: Optional[str] = None,
                          fecha: Optional[str] = None) -> Ingreso:
        """
        Actualiza un ingreso existente.
        
        Args:
            ingreso: Ingreso a actualizar
            monto: Nuevo monto (opcional)
            descripcion: Nueva descripción (opcional)
            categoria: Nueva categoría (opcional)
            fecha: Nueva fecha (opcional)
            
        Returns:
            Ingreso actualizado
            
        Raises:
            ValidationError: Si los datos no son válidos
        """
        if monto is not None:
            es_valido, error, monto_decimal = validate_monto(monto)
            if not es_valido:
                raise ValidationError(error)
            ingreso.monto = monto_decimal
        
        if descripcion is not None:
            es_valido, error = validate_texto(descripcion, "Descripción", max_length=255)
            if not es_valido:
                raise ValidationError(error)
            ingreso.descripcion = descripcion
        
        if categoria is not None:
            es_valido, error = validate_categoria(categoria, 'ingreso')
            if not es_valido:
                raise ValidationError(error)
            ingreso.categoria = categoria
        
        if fecha is not None:
            es_valido, error, fecha_date = validate_fecha(fecha)
            if not es_valido:
                raise ValidationError(error)
            ingreso.fecha = fecha_date
        
        db.session.commit()
        return ingreso
    
    @staticmethod
    def eliminar_ingreso(ingreso: Ingreso) -> None:
        """
        Elimina un ingreso.
        
        Args:
            ingreso: Ingreso a eliminar
        """
        db.session.delete(ingreso)
        db.session.commit()
    
    @staticmethod
    def crear_egreso(usuario_id: int, monto: str, descripcion: str,
                    categoria: str, fecha: str) -> Egreso:
        """
        Crea un nuevo egreso.
        
        Args:
            usuario_id: ID del usuario
            monto: Monto del egreso
            descripcion: Descripción del egreso
            categoria: Categoría del egreso
            fecha: Fecha del egreso (formato YYYY-MM-DD)
            
        Returns:
            Egreso creado
            
        Raises:
            ValidationError: Si los datos no son válidos
        """
        # Validar datos
        es_valido, error, monto_decimal = validate_monto(monto)
        if not es_valido:
            raise ValidationError(error)
        
        es_valido, error, fecha_date = validate_fecha(fecha)
        if not es_valido:
            raise ValidationError(error)
        
        es_valido, error = validate_texto(descripcion, "Descripción", max_length=255)
        if not es_valido:
            raise ValidationError(error)
        
        es_valido, error = validate_categoria(categoria, 'egreso')
        if not es_valido:
            raise ValidationError(error)
        
        # Crear egreso
        egreso = Egreso(
            usuario_id=usuario_id,
            monto=monto_decimal,
            descripcion=descripcion,
            categoria=categoria,
            fecha=fecha_date
        )
        
        db.session.add(egreso)
        db.session.commit()
        
        return egreso
    
    @staticmethod
    def actualizar_egreso(egreso: Egreso, monto: Optional[str] = None,
                          descripcion: Optional[str] = None,
                          categoria: Optional[str] = None,
                          fecha: Optional[str] = None) -> Egreso:
        """
        Actualiza un egreso existente.
        
        Args:
            egreso: Egreso a actualizar
            monto: Nuevo monto (opcional)
            descripcion: Nueva descripción (opcional)
            categoria: Nueva categoría (opcional)
            fecha: Nueva fecha (opcional)
            
        Returns:
            Egreso actualizado
            
        Raises:
            ValidationError: Si los datos no son válidos
        """
        if monto is not None:
            es_valido, error, monto_decimal = validate_monto(monto)
            if not es_valido:
                raise ValidationError(error)
            egreso.monto = monto_decimal
        
        if descripcion is not None:
            es_valido, error = validate_texto(descripcion, "Descripción", max_length=255)
            if not es_valido:
                raise ValidationError(error)
            egreso.descripcion = descripcion
        
        if categoria is not None:
            es_valido, error = validate_categoria(categoria, 'egreso')
            if not es_valido:
                raise ValidationError(error)
            egreso.categoria = categoria
        
        if fecha is not None:
            es_valido, error, fecha_date = validate_fecha(fecha)
            if not es_valido:
                raise ValidationError(error)
            egreso.fecha = fecha_date
        
        db.session.commit()
        return egreso
    
    @staticmethod
    def eliminar_egreso(egreso: Egreso) -> None:
        """
        Elimina un egreso.
        
        Args:
            egreso: Egreso a eliminar
        """
        db.session.delete(egreso)
        db.session.commit()


