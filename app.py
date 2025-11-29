"""
Aplicación principal Flask.

Este módulo inicializa la aplicación Flask y configura todos los componentes.
"""
from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, date
from database import db
from config import get_config
from utils.error_handler import register_error_handlers


def create_app(config_class=None):
    """
    Factory function para crear la aplicación Flask.
    
    Args:
        config_class: Clase de configuración a usar (opcional)
        
    Returns:
        Instancia de Flask configurada
    """
    app = Flask(__name__)
    
    # Cargar configuración
    if config_class is None:
        config_class = get_config()
    app.config.from_object(config_class)
    
    # Inicializar extensiones
    db.init_app(app)
    migrate = Migrate(app, db)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
    
    mail = Mail(app)
    
    # Configurar scheduler para tareas programadas
    scheduler = BackgroundScheduler()
    scheduler.start()
    
    # Importar modelos después de inicializar db
    from models import User, Ingreso, Egreso, Meta, Ahorro, Recordatorio, DeudaFija
    
    @login_manager.user_loader
    def load_user(user_id):
        """Carga un usuario por su ID."""
        return User.query.get(int(user_id))
    
    def verificar_recordatorios():
        """Tarea programada para verificar y enviar recordatorios."""
        with app.app_context():
            from datetime import timedelta
            hoy = datetime.now().date()
            
            # Verificar recordatorios normales
            recordatorios = Recordatorio.query.filter_by(enviado=False).all()
            
            for recordatorio in recordatorios:
                if recordatorio.fecha_recordatorio <= hoy:
                    try:
                        from flask_mail import Message
                        msg = Message(
                            subject=f'[FINANZAS MALU] Recordatorio: {recordatorio.titulo}',
                            recipients=[recordatorio.usuario.email],
                            body=f'Hola {recordatorio.usuario.nombre},\n\n'
                                 f'Te recordamos que tienes un pago pendiente:\n\n'
                                 f'Título: {recordatorio.titulo}\n'
                                 f'Descripción: {recordatorio.descripcion}\n'
                                 f'Fecha de pago: {recordatorio.fecha_pago}\n'
                                 f'Monto: ${recordatorio.monto:.2f}\n\n'
                                 f'Por favor, no olvides realizar este pago a tiempo.'
                        )
                        mail.send(msg)
                        recordatorio.enviado = True
                        db.session.commit()
                    except Exception as e:
                        app.logger.error(f'Error enviando recordatorio: {e}')
            
            # Verificar deudas fijas (2 días antes)
            deudas = DeudaFija.query.filter_by(activa=True, pagada_este_mes=False).all()
            
            for deuda in deudas:
                # Calcular fecha de pago del mes actual
                fecha_pago_mes = date(hoy.year, hoy.month, min(deuda.dia_pago, 28))
                if fecha_pago_mes < hoy:
                    # Si ya pasó, usar el próximo mes
                    if hoy.month == 12:
                        fecha_pago_mes = date(hoy.year + 1, 1, min(deuda.dia_pago, 28))
                    else:
                        fecha_pago_mes = date(hoy.year, hoy.month + 1, min(deuda.dia_pago, 28))
                
                # Verificar si faltan 2 días o menos
                dias_restantes = (fecha_pago_mes - hoy).days
                
                if 0 <= dias_restantes <= 2:
                    # Verificar si ya se envió notificación hoy
                    try:
                        from models import TokenRecuperacion
                        # Usar un campo temporal o verificar última notificación
                        # Por simplicidad, enviaremos si está en el rango
                        from flask_mail import Message
                        msg = Message(
                            subject=f'[FINANZAS MALU] Recordatorio: Pago de deuda fija - {deuda.titulo}',
                            recipients=[deuda.usuario.email],
                            body=f'Hola {deuda.usuario.nombre},\n\n'
                                 f'Te recordamos que tienes una deuda fija próxima a vencer:\n\n'
                                 f'Deuda: {deuda.titulo}\n'
                                 f'Descripción: {deuda.descripcion or "Sin descripción"}\n'
                                 f'Fecha de pago: {fecha_pago_mes.strftime("%d/%m/%Y")}\n'
                                 f'Monto: ${deuda.monto:.2f}\n'
                                 f'Días restantes: {dias_restantes}\n\n'
                                 f'Por favor, no olvides realizar este pago a tiempo.\n'
                                 f'Puedes marcarlo como pagado en la aplicación cuando lo realices.'
                        )
                        mail.send(msg)
                        app.logger.info(f'Notificación de deuda enviada: {deuda.titulo}')
                    except Exception as e:
                        app.logger.error(f'Error enviando notificación de deuda: {e}')
    
    # Programar verificación diaria de recordatorios
    scheduler.add_job(
        func=verificar_recordatorios,
        trigger='cron',
        hour=app.config.get('SCHEDULER_HOUR', 9),
        minute=app.config.get('SCHEDULER_MINUTE', 0),
        id='verificar_recordatorios',
        name='Verificar recordatorios diarios',
        replace_existing=True
    )
    
    # Registrar blueprints
    from routes.auth import auth_bp
    from routes.main import main_bp
    from routes.transacciones import transacciones_bp
    from routes.metas import metas_bp
    from routes.ahorros import ahorros_bp
    from routes.recordatorios import recordatorios_bp
    from routes.deudas import deudas_bp
    from routes.estrategias import estrategias_bp
    from routes.api import api_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(transacciones_bp)
    app.register_blueprint(metas_bp)
    app.register_blueprint(ahorros_bp)
    app.register_blueprint(recordatorios_bp)
    app.register_blueprint(deudas_bp)
    app.register_blueprint(estrategias_bp)
    app.register_blueprint(api_bp)
    
    # Registrar manejadores de errores
    register_error_handlers(app)
    
    # Agregar funciones globales a Jinja2
    @app.context_processor
    def inject_date():
        """Inyecta funciones útiles en todos los templates."""
        from datetime import date as date_class
        return dict(date=date_class, min=min, max=max)
    
    return app


# Crear instancia de la aplicación
app = create_app()


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=app.config.get('DEBUG', False), 
            host='0.0.0.0', 
            port=5000)
