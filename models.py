from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date, timedelta
from database import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    ingresos = db.relationship('Ingreso', backref='usuario', lazy=True, cascade='all, delete-orphan')
    egresos = db.relationship('Egreso', backref='usuario', lazy=True, cascade='all, delete-orphan')
    metas = db.relationship('Meta', backref='usuario', lazy=True, cascade='all, delete-orphan')
    ahorros = db.relationship('Ahorro', backref='usuario', lazy=True, cascade='all, delete-orphan')
    recordatorios = db.relationship('Recordatorio', backref='usuario', lazy=True, cascade='all, delete-orphan')
    deudas_fijas = db.relationship('DeudaFija', backref='usuario', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.email}>'

class Ingreso(db.Model):
    __tablename__ = 'ingresos'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    monto = db.Column(db.Numeric(10, 2), nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.Date, nullable=False, default=date.today)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Ingreso {self.monto} - {self.descripcion}>'

class Egreso(db.Model):
    __tablename__ = 'egresos'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    monto = db.Column(db.Numeric(10, 2), nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.Date, nullable=False, default=date.today)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Egreso {self.monto} - {self.descripcion}>'

class Meta(db.Model):
    __tablename__ = 'metas'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    monto_objetivo = db.Column(db.Numeric(10, 2), nullable=False)
    monto_actual = db.Column(db.Numeric(10, 2), default=0.00)
    fecha_limite = db.Column(db.Date, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    completada = db.Column(db.Boolean, default=False)
    
    def porcentaje_completado(self):
        if self.monto_objetivo > 0:
            return min(100, (float(self.monto_actual) / float(self.monto_objetivo)) * 100)
        return 0
    
    def __repr__(self):
        return f'<Meta {self.titulo}>'

class Ahorro(db.Model):
    __tablename__ = 'ahorros'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    monto = db.Column(db.Numeric(10, 2), nullable=False)
    frecuencia = db.Column(db.String(20), nullable=False, default='mensual')  # diaria, semanal, mensual, anual
    fecha_inicio = db.Column(db.Date, nullable=False, default=date.today)
    fecha_fin = db.Column(db.Date)
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Ahorro {self.titulo}>'

class TokenRecuperacion(db.Model):
    __tablename__ = 'tokens_recuperacion'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    token = db.Column(db.String(100), unique=True, nullable=False)
    fecha_expiracion = db.Column(db.DateTime, nullable=False)
    usado = db.Column(db.Boolean, default=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    usuario = db.relationship('User', backref='tokens_recuperacion')
    
    def __repr__(self):
        return f'<TokenRecuperacion {self.token}>'

class Recordatorio(db.Model):
    __tablename__ = 'recordatorios'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    monto = db.Column(db.Numeric(10, 2), nullable=False)
    fecha_pago = db.Column(db.Date, nullable=False)
    fecha_recordatorio = db.Column(db.Date, nullable=False)
    enviado = db.Column(db.Boolean, default=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Recordatorio {self.titulo}>'

class DeudaFija(db.Model):
    __tablename__ = 'deudas_fijas'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    monto = db.Column(db.Numeric(10, 2), nullable=False)
    fecha_pago = db.Column(db.Date, nullable=False)  # Fecha de pago mensual
    dia_pago = db.Column(db.Integer, nullable=False)  # Día del mes (1-31)
    activa = db.Column(db.Boolean, default=True)
    pagada_este_mes = db.Column(db.Boolean, default=False)
    fecha_ultimo_pago = db.Column(db.Date)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # La relación 'usuario' se crea automáticamente a través del backref en User
    
    def necesita_pago(self):
        """Verifica si la deuda necesita pago este mes."""
        hoy = date.today()
        # Si ya está pagada este mes, no necesita pago
        if self.pagada_este_mes and self.fecha_ultimo_pago:
            if self.fecha_ultimo_pago.year == hoy.year and self.fecha_ultimo_pago.month == hoy.month:
                return False
        
        # Calcular fecha de pago del mes actual
        fecha_pago_mes = date(hoy.year, hoy.month, min(self.dia_pago, 28))
        if fecha_pago_mes < hoy:
            # Si ya pasó, usar el próximo mes
            if hoy.month == 12:
                fecha_pago_mes = date(hoy.year + 1, 1, min(self.dia_pago, 28))
            else:
                fecha_pago_mes = date(hoy.year, hoy.month + 1, min(self.dia_pago, 28))
        
        # Verificar si faltan 2 días o menos
        dias_restantes = (fecha_pago_mes - hoy).days
        return 0 <= dias_restantes <= 2 and not self.pagada_este_mes
    
    def __repr__(self):
        return f'<DeudaFija {self.titulo}>'

