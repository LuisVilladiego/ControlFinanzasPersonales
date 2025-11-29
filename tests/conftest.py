"""
Configuración de pytest.

Define fixtures compartidas para todas las pruebas.
"""
import pytest
from app import create_app
from database import db
from models import User
from config import TestingConfig


@pytest.fixture
def app():
    """Crea una instancia de la aplicación para pruebas."""
    app = create_app(TestingConfig)
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def app():
    """Crea una instancia de la aplicación para pruebas."""
    app = create_app(TestingConfig)
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """Cliente de prueba para hacer requests."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Runner para comandos CLI."""
    return app.test_cli_runner()


@pytest.fixture
def usuario_test(app):
    """Crea un usuario de prueba."""
    with app.app_context():
        usuario = User(
            nombre='Usuario Test',
            email='test@example.com'
        )
        usuario.set_password('password123')
        db.session.add(usuario)
        db.session.commit()
        return usuario


@pytest.fixture
def usuario_autenticado(client, usuario_test):
    """Autentica un usuario para las pruebas."""
    client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password123'
    })
    return usuario_test

