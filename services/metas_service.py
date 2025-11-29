"""
Servicio de metas financieras.

Contiene la lógica de negocio para metas de ahorro.
"""
from typing import Optional
from decimal import Decimal
from datetime import date
from database import db
from models import Meta
from services.validators import (
    validate_monto, validate_fecha, validate_texto,
    validate_fecha_limite, ValidationError
)


class MetasService:
    """Servicio para gestionar metas financieras."""
    
    @staticmethod
    def crear_meta(usuario_id: int, titulo: str, monto_objetivo: str,
                  fecha_limite: str, descripcion: Optional[str] = None) -> Meta:
        """
        Crea una nueva meta financiera.
        
        Args:
            usuario_id: ID del usuario
            titulo: Título de la meta
            monto_objetivo: Monto objetivo
            fecha_limite: Fecha límite (formato YYYY-MM-DD)
            descripcion: Descripción opcional
            
        Returns:
            Meta creada
            
        Raises:
            ValidationError: Si los datos no son válidos
        """
        # Validar datos
        es_valido, error = validate_texto(titulo, "Título", max_length=200)
        if not es_valido:
            raise ValidationError(error)
        
        es_valido, error, monto_decimal = validate_monto(monto_objetivo)
        if not es_valido:
            raise ValidationError(error)
        
        es_valido, error, fecha_date = validate_fecha(fecha_limite)
        if not es_valido:
            raise ValidationError(error)
        
        es_valido, error = validate_fecha_limite(fecha_date)
        if not es_valido:
            raise ValidationError(error)
        
        if descripcion:
            es_valido, error = validate_texto(descripcion, "Descripción", 
                                            max_length=1000, required=False)
            if not es_valido:
                raise ValidationError(error)
        
        # Crear meta
        meta = Meta(
            usuario_id=usuario_id,
            titulo=titulo,
            descripcion=descripcion or '',
            monto_objetivo=monto_decimal,
            fecha_limite=fecha_date
        )
        
        db.session.add(meta)
        db.session.commit()
        
        return meta
    
    @staticmethod
    def actualizar_meta(meta: Meta, titulo: Optional[str] = None,
                       monto_objetivo: Optional[str] = None,
                       fecha_limite: Optional[str] = None,
                       descripcion: Optional[str] = None) -> Meta:
        """
        Actualiza una meta existente.
        
        Args:
            meta: Meta a actualizar
            titulo: Nuevo título (opcional)
            monto_objetivo: Nuevo monto objetivo (opcional)
            fecha_limite: Nueva fecha límite (opcional)
            descripcion: Nueva descripción (opcional)
            
        Returns:
            Meta actualizada
            
        Raises:
            ValidationError: Si los datos no son válidos
        """
        if titulo is not None:
            es_valido, error = validate_texto(titulo, "Título", max_length=200)
            if not es_valido:
                raise ValidationError(error)
            meta.titulo = titulo
        
        if monto_objetivo is not None:
            es_valido, error, monto_decimal = validate_monto(monto_objetivo)
            if not es_valido:
                raise ValidationError(error)
            meta.monto_objetivo = monto_decimal
        
        if fecha_limite is not None:
            es_valido, error, fecha_date = validate_fecha(fecha_limite)
            if not es_valido:
                raise ValidationError(error)
            es_valido, error = validate_fecha_limite(fecha_date)
            if not es_valido:
                raise ValidationError(error)
            meta.fecha_limite = fecha_date
        
        if descripcion is not None:
            es_valido, error = validate_texto(descripcion, "Descripción",
                                            max_length=1000, required=False)
            if not es_valido:
                raise ValidationError(error)
            meta.descripcion = descripcion
        
        db.session.commit()
        return meta
    
    @staticmethod
    def agregar_monto(meta: Meta, monto: str) -> Meta:
        """
        Agrega un monto a una meta.
        
        Args:
            meta: Meta a actualizar
            monto: Monto a agregar
            
        Returns:
            Meta actualizada
            
        Raises:
            ValidationError: Si el monto no es válido
        """
        es_valido, error, monto_decimal = validate_monto(monto)
        if not es_valido:
            raise ValidationError(error)
        
        # Asegurar que ambos sean Decimal
        from decimal import Decimal
        if not isinstance(meta.monto_actual, Decimal):
            meta.monto_actual = Decimal(str(meta.monto_actual))
        if not isinstance(monto_decimal, Decimal):
            monto_decimal = Decimal(str(monto_decimal))
        
        meta.monto_actual += monto_decimal
        
        # Verificar si la meta está completada
        if meta.monto_actual >= meta.monto_objetivo:
            meta.monto_actual = meta.monto_objetivo
            meta.completada = True
        
        db.session.commit()
        return meta
    
    @staticmethod
    def eliminar_meta(meta: Meta) -> None:
        """
        Elimina una meta.
        
        Args:
            meta: Meta a eliminar
        """
        db.session.delete(meta)
        db.session.commit()

