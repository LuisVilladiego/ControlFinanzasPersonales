"""
Pruebas para autenticación.
"""
import pytest
from models import User
from database import db


class TestAuth:
    """Pruebas para el sistema de autenticación."""
    
    def test_registro_usuario(self, client):
        """Prueba el registro de un nuevo usuario."""
        response = client.post('/registro', data={
            'nombre': 'Nuevo Usuario',
            'email': 'nuevo@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        # Verificar que el usuario fue creado
        with client.application.app_context():
            usuario = User.query.filter_by(email='nuevo@example.com').first()
            assert usuario is not None
            assert usuario.nombre == 'Nuevo Usuario'
    
    def test_login_exitoso(self, client, usuario_test):
        """Prueba el inicio de sesión exitoso."""
        response = client.post('/login', data={
            'email': 'test@example.com',
            'password': 'password123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
    
    def test_login_credenciales_invalidas(self, client, usuario_test):
        """Prueba el inicio de sesión con credenciales inválidas."""
        response = client.post('/login', data={
            'email': 'test@example.com',
            'password': 'password_incorrecta'
        })
        
        # Debe mostrar un mensaje de error
        assert b'incorrectos' in response.data.lower() or b'error' in response.data.lower()
    
    def test_logout(self, client, usuario_autenticado):
        """Prueba el cierre de sesión."""
        response = client.get('/logout', follow_redirects=True)
        assert response.status_code == 200


