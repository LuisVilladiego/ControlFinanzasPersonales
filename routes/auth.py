from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
from models import User, TokenRecuperacion
from database import db
from datetime import datetime, timedelta
import secrets

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not nombre or not email or not password:
            flash('Por favor completa todos los campos.', 'error')
            return render_template('auth/registro.html')
        
        if password != confirm_password:
            flash('Las contraseñas no coinciden.', 'error')
            return render_template('auth/registro.html')
        
        if User.query.filter_by(email=email).first():
            flash('El email ya está registrado.', 'error')
            return render_template('auth/registro.html')
        
        usuario = User(nombre=nombre, email=email)
        usuario.set_password(password)
        db.session.add(usuario)
        db.session.commit()
        
        flash('Registro exitoso. Por favor inicia sesión.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/registro.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Por favor completa todos los campos.', 'error')
            return render_template('auth/login.html')
        
        usuario = User.query.filter_by(email=email).first()
        
        if usuario and usuario.check_password(password):
            login_user(usuario)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        else:
            flash('Email o contraseña incorrectos.', 'error')
    
    return render_template('auth/login.html')

@auth_bp.route('/recuperar-contraseña', methods=['GET', 'POST'])
def recuperar_contraseña():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        
        if not email:
            flash('Por favor ingresa tu email.', 'error')
            return render_template('auth/recuperar_contraseña.html')
        
        usuario = User.query.filter_by(email=email).first()
        
        if usuario:
            # Generar token de recuperación
            token = secrets.token_urlsafe(32)
            fecha_expiracion = datetime.utcnow() + timedelta(hours=24)
            
            # Eliminar tokens anteriores del usuario
            TokenRecuperacion.query.filter_by(usuario_id=usuario.id, usado=False).delete()
            
            token_rec = TokenRecuperacion(
                usuario_id=usuario.id,
                token=token,
                fecha_expiracion=fecha_expiracion
            )
            db.session.add(token_rec)
            db.session.commit()
            
            # Enviar email
            try:
                reset_url = url_for('auth.resetear_contraseña', token=token, _external=True)
                msg = Message(
                    subject='Recuperación de Contraseña - FINANZAS MALU',
                    recipients=[usuario.email],
                    body=f'Hola {usuario.nombre},\n\n'
                         f'Has solicitado recuperar tu contraseña. '
                         f'Para restablecer tu contraseña, haz clic en el siguiente enlace:\n\n'
                         f'{reset_url}\n\n'
                         f'Este enlace expirará en 24 horas.\n\n'
                         f'Si no solicitaste este cambio, ignora este mensaje.'
                )
                # Obtener mail desde current_app
                from flask import current_app
                mail = current_app.extensions.get('mail')
                if mail:
                    mail.send(msg)
                    flash('Se ha enviado un enlace de recuperación a tu email.', 'success')
                else:
                    flash('Error: servicio de email no configurado.', 'error')
            except Exception as e:
                flash(f'Error al enviar el email: {str(e)}', 'error')
        else:
            # Por seguridad, mostrar el mismo mensaje aunque el email no exista
            flash('Si el email existe, se ha enviado un enlace de recuperación.', 'success')
    
    return render_template('auth/recuperar_contraseña.html')

@auth_bp.route('/resetear-contraseña/<token>', methods=['GET', 'POST'])
def resetear_contraseña(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    token_rec = TokenRecuperacion.query.filter_by(token=token, usado=False).first()
    
    if not token_rec or token_rec.fecha_expiracion < datetime.utcnow():
        flash('El enlace de recuperación es inválido o ha expirado.', 'error')
        return redirect(url_for('auth.recuperar_contraseña'))
    
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not password or not confirm_password:
            flash('Por favor completa todos los campos.', 'error')
            return render_template('auth/resetear_contraseña.html', token=token)
        
        if password != confirm_password:
            flash('Las contraseñas no coinciden.', 'error')
            return render_template('auth/resetear_contraseña.html', token=token)
        
        usuario = token_rec.usuario
        usuario.set_password(password)
        token_rec.usado = True
        db.session.commit()
        
        flash('Contraseña restablecida exitosamente. Por favor inicia sesión.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/resetear_contraseña.html', token=token)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente.', 'success')
    return redirect(url_for('auth.login'))
