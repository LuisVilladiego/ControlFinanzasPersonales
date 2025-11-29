"""
Manejo centralizado de errores.

Proporciona funciones y decoradores para manejar errores de manera consistente.
"""
from functools import wraps
from flask import jsonify, flash, redirect, url_for, request
from services.validators import ValidationError
from database import db


def handle_errors(f):
    """
    Decorador para manejar errores en rutas.
    
    Maneja ValidationError y otros errores de base de datos.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValidationError as e:
            flash(str(e), 'error')
            db.session.rollback()
            # Intentar redirigir a la página anterior o dashboard
            return redirect(request.referrer or url_for('main.dashboard'))
        except Exception as e:
            flash(f'Error inesperado: {str(e)}', 'error')
            db.session.rollback()
            return redirect(request.referrer or url_for('main.dashboard'))
    return decorated_function


def handle_api_errors(f):
    """
    Decorador para manejar errores en endpoints de API.
    
    Retorna respuestas JSON apropiadas para errores.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValidationError as e:
            return jsonify({'error': str(e)}), 400
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Error interno del servidor'}), 500
    return decorated_function


def register_error_handlers(app):
    """
    Registra manejadores de errores globales para la aplicación.
    
    Args:
        app: Instancia de Flask
    """
    @app.errorhandler(404)
    def not_found(error):
        """Maneja errores 404."""
        return jsonify({'error': 'Recurso no encontrado'}), 404
    
    @app.errorhandler(403)
    def forbidden(error):
        """Maneja errores 403."""
        return jsonify({'error': 'No autorizado'}), 403
    
    @app.errorhandler(500)
    def internal_error(error):
        """Maneja errores 500."""
        db.session.rollback()
        return jsonify({'error': 'Error interno del servidor'}), 500

