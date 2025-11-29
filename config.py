"""
Configuración de la aplicación Flask.

Este módulo maneja todas las configuraciones de la aplicación,
incluyendo variables de entorno y configuraciones por defecto.
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuración base de la aplicación."""
    
    # Configuración de seguridad
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Configuración de base de datos
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///finanzas.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = os.getenv('SQLALCHEMY_ECHO', 'False').lower() == 'true'
    
    # Configuración de email
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', '')
    
    # Configuración de scheduler
    SCHEDULER_TIMEZONE = os.getenv('SCHEDULER_TIMEZONE', 'UTC')
    SCHEDULER_HOUR = int(os.getenv('SCHEDULER_HOUR', 9))
    SCHEDULER_MINUTE = int(os.getenv('SCHEDULER_MINUTE', 0))
    
    # Configuración de paginación
    ITEMS_PER_PAGE = int(os.getenv('ITEMS_PER_PAGE', 10))
    
    # Configuración de tokens
    TOKEN_EXPIRATION_HOURS = int(os.getenv('TOKEN_EXPIRATION_HOURS', 24))


class DevelopmentConfig(Config):
    """Configuración para desarrollo."""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Configuración para producción."""
    DEBUG = False
    TESTING = False
    
    def __init__(self):
        """Valida configuración al instanciar."""
        super().__init__()
        # En producción, SECRET_KEY debe estar definida
        if self.SECRET_KEY == 'dev-secret-key-change-in-production':
            raise ValueError("SECRET_KEY debe estar configurada en producción")


class TestingConfig(Config):
    """Configuración para pruebas."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


# Diccionario de configuraciones
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config():
    """Obtiene la configuración según el entorno."""
    env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])

