from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models import Ingreso, Egreso, Meta, Ahorro, Recordatorio
from database import db
from datetime import datetime
from functools import wraps

api_bp = Blueprint('api', __name__, url_prefix='/api')

def json_response(func):
    """Decorador para manejar respuestas JSON"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            if isinstance(result, tuple):
                return result
            return jsonify(result), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    return wrapper

# ========== INGRESOS ==========
@api_bp.route('/ingresos', methods=['GET'])
@login_required
@json_response
def listar_ingresos():
    ingresos = Ingreso.query.filter_by(usuario_id=current_user.id).all()
    return {
        'ingresos': [{
            'id': i.id,
            'monto': float(i.monto),
            'descripcion': i.descripcion,
            'categoria': i.categoria,
            'fecha': i.fecha.isoformat()
        } for i in ingresos]
    }

@api_bp.route('/ingresos', methods=['POST'])
@login_required
@json_response
def crear_ingreso():
    data = request.get_json()
    ingreso = Ingreso(
        usuario_id=current_user.id,
        monto=float(data['monto']),
        descripcion=data['descripcion'],
        categoria=data['categoria'],
        fecha=datetime.strptime(data['fecha'], '%Y-%m-%d').date()
    )
    db.session.add(ingreso)
    db.session.commit()
    return {'message': 'Ingreso creado exitosamente', 'id': ingreso.id}

@api_bp.route('/ingresos/<int:id>', methods=['GET'])
@login_required
def obtener_ingreso(id):
    ingreso = Ingreso.query.get_or_404(id)
    if ingreso.usuario_id != current_user.id:
        return jsonify({'error': 'No autorizado'}), 403
    return jsonify({
        'id': ingreso.id,
        'monto': float(ingreso.monto),
        'descripcion': ingreso.descripcion,
        'categoria': ingreso.categoria,
        'fecha': ingreso.fecha.isoformat()
    })

@api_bp.route('/ingresos/<int:id>', methods=['PUT'])
@login_required
def actualizar_ingreso(id):
    ingreso = Ingreso.query.get_or_404(id)
    if ingreso.usuario_id != current_user.id:
        return jsonify({'error': 'No autorizado'}), 403
    
    data = request.get_json()
    ingreso.monto = float(data.get('monto', ingreso.monto))
    ingreso.descripcion = data.get('descripcion', ingreso.descripcion)
    ingreso.categoria = data.get('categoria', ingreso.categoria)
    if 'fecha' in data:
        ingreso.fecha = datetime.strptime(data['fecha'], '%Y-%m-%d').date()
    
    db.session.commit()
    return jsonify({'message': 'Ingreso actualizado exitosamente'})

@api_bp.route('/ingresos/<int:id>', methods=['DELETE'])
@login_required
def eliminar_ingreso(id):
    ingreso = Ingreso.query.get_or_404(id)
    if ingreso.usuario_id != current_user.id:
        return jsonify({'error': 'No autorizado'}), 403
    
    db.session.delete(ingreso)
    db.session.commit()
    return jsonify({'message': 'Ingreso eliminado exitosamente'})

# ========== EGRESOS ==========
@api_bp.route('/egresos', methods=['GET'])
@login_required
@json_response
def listar_egresos():
    egresos = Egreso.query.filter_by(usuario_id=current_user.id).all()
    return {
        'egresos': [{
            'id': e.id,
            'monto': float(e.monto),
            'descripcion': e.descripcion,
            'categoria': e.categoria,
            'fecha': e.fecha.isoformat()
        } for e in egresos]
    }

@api_bp.route('/egresos', methods=['POST'])
@login_required
@json_response
def crear_egreso():
    data = request.get_json()
    egreso = Egreso(
        usuario_id=current_user.id,
        monto=float(data['monto']),
        descripcion=data['descripcion'],
        categoria=data['categoria'],
        fecha=datetime.strptime(data['fecha'], '%Y-%m-%d').date()
    )
    db.session.add(egreso)
    db.session.commit()
    return {'message': 'Egreso creado exitosamente', 'id': egreso.id}

@api_bp.route('/egresos/<int:id>', methods=['GET'])
@login_required
def obtener_egreso(id):
    egreso = Egreso.query.get_or_404(id)
    if egreso.usuario_id != current_user.id:
        return jsonify({'error': 'No autorizado'}), 403
    return jsonify({
        'id': egreso.id,
        'monto': float(egreso.monto),
        'descripcion': egreso.descripcion,
        'categoria': egreso.categoria,
        'fecha': egreso.fecha.isoformat()
    })

@api_bp.route('/egresos/<int:id>', methods=['PUT'])
@login_required
def actualizar_egreso(id):
    egreso = Egreso.query.get_or_404(id)
    if egreso.usuario_id != current_user.id:
        return jsonify({'error': 'No autorizado'}), 403
    
    data = request.get_json()
    egreso.monto = float(data.get('monto', egreso.monto))
    egreso.descripcion = data.get('descripcion', egreso.descripcion)
    egreso.categoria = data.get('categoria', egreso.categoria)
    if 'fecha' in data:
        egreso.fecha = datetime.strptime(data['fecha'], '%Y-%m-%d').date()
    
    db.session.commit()
    return jsonify({'message': 'Egreso actualizado exitosamente'})

@api_bp.route('/egresos/<int:id>', methods=['DELETE'])
@login_required
def eliminar_egreso(id):
    egreso = Egreso.query.get_or_404(id)
    if egreso.usuario_id != current_user.id:
        return jsonify({'error': 'No autorizado'}), 403
    
    db.session.delete(egreso)
    db.session.commit()
    return jsonify({'message': 'Egreso eliminado exitosamente'})

# ========== METAS ==========
@api_bp.route('/metas', methods=['GET'])
@login_required
@json_response
def listar_metas():
    metas = Meta.query.filter_by(usuario_id=current_user.id).all()
    return {
        'metas': [{
            'id': m.id,
            'titulo': m.titulo,
            'descripcion': m.descripcion,
            'monto_objetivo': float(m.monto_objetivo),
            'monto_actual': float(m.monto_actual),
            'fecha_limite': m.fecha_limite.isoformat(),
            'completada': m.completada,
            'porcentaje': m.porcentaje_completado()
        } for m in metas]
    }

@api_bp.route('/metas', methods=['POST'])
@login_required
@json_response
def crear_meta():
    data = request.get_json()
    meta = Meta(
        usuario_id=current_user.id,
        titulo=data['titulo'],
        descripcion=data.get('descripcion', ''),
        monto_objetivo=float(data['monto_objetivo']),
        fecha_limite=datetime.strptime(data['fecha_limite'], '%Y-%m-%d').date()
    )
    db.session.add(meta)
    db.session.commit()
    return {'message': 'Meta creada exitosamente', 'id': meta.id}

@api_bp.route('/metas/<int:id>', methods=['PUT'])
@login_required
def actualizar_meta(id):
    meta = Meta.query.get_or_404(id)
    if meta.usuario_id != current_user.id:
        return jsonify({'error': 'No autorizado'}), 403
    
    data = request.get_json()
    meta.titulo = data.get('titulo', meta.titulo)
    meta.descripcion = data.get('descripcion', meta.descripcion)
    meta.monto_objetivo = float(data.get('monto_objetivo', meta.monto_objetivo))
    if 'fecha_limite' in data:
        meta.fecha_limite = datetime.strptime(data['fecha_limite'], '%Y-%m-%d').date()
    if 'monto_actual' in data:
        meta.monto_actual = float(data['monto_actual'])
        if meta.monto_actual >= meta.monto_objetivo:
            meta.completada = True
    
    db.session.commit()
    return jsonify({'message': 'Meta actualizada exitosamente'})

@api_bp.route('/metas/<int:id>', methods=['DELETE'])
@login_required
def eliminar_meta(id):
    meta = Meta.query.get_or_404(id)
    if meta.usuario_id != current_user.id:
        return jsonify({'error': 'No autorizado'}), 403
    
    db.session.delete(meta)
    db.session.commit()
    return jsonify({'message': 'Meta eliminada exitosamente'})

# ========== AHORROS ==========
@api_bp.route('/ahorros', methods=['GET'])
@login_required
@json_response
def listar_ahorros():
    ahorros = Ahorro.query.filter_by(usuario_id=current_user.id).all()
    return {
        'ahorros': [{
            'id': a.id,
            'titulo': a.titulo,
            'descripcion': a.descripcion,
            'monto': float(a.monto),
            'frecuencia': a.frecuencia,
            'fecha_inicio': a.fecha_inicio.isoformat(),
            'fecha_fin': a.fecha_fin.isoformat() if a.fecha_fin else None,
            'activo': a.activo
        } for a in ahorros]
    }

@api_bp.route('/ahorros', methods=['POST'])
@login_required
@json_response
def crear_ahorro():
    data = request.get_json()
    ahorro = Ahorro(
        usuario_id=current_user.id,
        titulo=data['titulo'],
        descripcion=data.get('descripcion', ''),
        monto=float(data['monto']),
        frecuencia=data.get('frecuencia', 'mensual'),
        fecha_inicio=datetime.strptime(data['fecha_inicio'], '%Y-%m-%d').date(),
        fecha_fin=datetime.strptime(data['fecha_fin'], '%Y-%m-%d').date() if data.get('fecha_fin') else None
    )
    db.session.add(ahorro)
    db.session.commit()
    return {'message': 'Ahorro creado exitosamente', 'id': ahorro.id}

@api_bp.route('/ahorros/<int:id>', methods=['PUT'])
@login_required
def actualizar_ahorro(id):
    ahorro = Ahorro.query.get_or_404(id)
    if ahorro.usuario_id != current_user.id:
        return jsonify({'error': 'No autorizado'}), 403
    
    data = request.get_json()
    ahorro.titulo = data.get('titulo', ahorro.titulo)
    ahorro.descripcion = data.get('descripcion', ahorro.descripcion)
    ahorro.monto = float(data.get('monto', ahorro.monto))
    ahorro.frecuencia = data.get('frecuencia', ahorro.frecuencia)
    if 'fecha_inicio' in data:
        ahorro.fecha_inicio = datetime.strptime(data['fecha_inicio'], '%Y-%m-%d').date()
    if 'fecha_fin' in data:
        ahorro.fecha_fin = datetime.strptime(data['fecha_fin'], '%Y-%m-%d').date() if data['fecha_fin'] else None
    if 'activo' in data:
        ahorro.activo = data['activo']
    
    db.session.commit()
    return jsonify({'message': 'Ahorro actualizado exitosamente'})

@api_bp.route('/ahorros/<int:id>', methods=['DELETE'])
@login_required
def eliminar_ahorro(id):
    ahorro = Ahorro.query.get_or_404(id)
    if ahorro.usuario_id != current_user.id:
        return jsonify({'error': 'No autorizado'}), 403
    
    db.session.delete(ahorro)
    db.session.commit()
    return jsonify({'message': 'Ahorro eliminado exitosamente'})

# ========== RECORDATORIOS ==========
@api_bp.route('/recordatorios', methods=['GET'])
@login_required
@json_response
def listar_recordatorios():
    recordatorios = Recordatorio.query.filter_by(usuario_id=current_user.id).all()
    return {
        'recordatorios': [{
            'id': r.id,
            'titulo': r.titulo,
            'descripcion': r.descripcion,
            'monto': float(r.monto),
            'fecha_pago': r.fecha_pago.isoformat(),
            'fecha_recordatorio': r.fecha_recordatorio.isoformat(),
            'enviado': r.enviado
        } for r in recordatorios]
    }

@api_bp.route('/recordatorios', methods=['POST'])
@login_required
@json_response
def crear_recordatorio():
    data = request.get_json()
    recordatorio = Recordatorio(
        usuario_id=current_user.id,
        titulo=data['titulo'],
        descripcion=data.get('descripcion', ''),
        monto=float(data['monto']),
        fecha_pago=datetime.strptime(data['fecha_pago'], '%Y-%m-%d').date(),
        fecha_recordatorio=datetime.strptime(data['fecha_recordatorio'], '%Y-%m-%d').date()
    )
    db.session.add(recordatorio)
    db.session.commit()
    return {'message': 'Recordatorio creado exitosamente', 'id': recordatorio.id}

@api_bp.route('/recordatorios/<int:id>', methods=['PUT'])
@login_required
def actualizar_recordatorio(id):
    recordatorio = Recordatorio.query.get_or_404(id)
    if recordatorio.usuario_id != current_user.id:
        return jsonify({'error': 'No autorizado'}), 403
    
    data = request.get_json()
    recordatorio.titulo = data.get('titulo', recordatorio.titulo)
    recordatorio.descripcion = data.get('descripcion', recordatorio.descripcion)
    recordatorio.monto = float(data.get('monto', recordatorio.monto))
    if 'fecha_pago' in data:
        recordatorio.fecha_pago = datetime.strptime(data['fecha_pago'], '%Y-%m-%d').date()
    if 'fecha_recordatorio' in data:
        recordatorio.fecha_recordatorio = datetime.strptime(data['fecha_recordatorio'], '%Y-%m-%d').date()
    
    db.session.commit()
    return jsonify({'message': 'Recordatorio actualizado exitosamente'})

@api_bp.route('/recordatorios/<int:id>', methods=['DELETE'])
@login_required
def eliminar_recordatorio(id):
    recordatorio = Recordatorio.query.get_or_404(id)
    if recordatorio.usuario_id != current_user.id:
        return jsonify({'error': 'No autorizado'}), 403
    
    db.session.delete(recordatorio)
    db.session.commit()
    return jsonify({'message': 'Recordatorio eliminado exitosamente'})

# ========== ESTADÍSTICAS ==========
@api_bp.route('/estadisticas', methods=['GET'])
@login_required
@json_response
def obtener_estadisticas():
    from datetime import date, timedelta
    from sqlalchemy import func
    
    hoy = date.today()
    inicio_mes = date(hoy.year, hoy.month, 1)
    
    ingresos_mes = db.session.query(func.sum(Ingreso.monto)).filter(
        Ingreso.usuario_id == current_user.id,
        Ingreso.fecha >= inicio_mes
    ).scalar() or 0
    
    egresos_mes = db.session.query(func.sum(Egreso.monto)).filter(
        Egreso.usuario_id == current_user.id,
        Egreso.fecha >= inicio_mes
    ).scalar() or 0
    
    balance_mes = float(ingresos_mes) - float(egresos_mes)
    
    return {
        'ingresos_mes': float(ingresos_mes),
        'egresos_mes': float(egresos_mes),
        'balance_mes': balance_mes,
        'total_metas': Meta.query.filter_by(usuario_id=current_user.id).count(),
        'metas_completadas': Meta.query.filter_by(usuario_id=current_user.id, completada=True).count()
    }

