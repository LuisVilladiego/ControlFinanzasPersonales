from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import Ahorro
from database import db
from datetime import datetime, date

ahorros_bp = Blueprint('ahorros', __name__)

@ahorros_bp.route('/ahorros')
@login_required
def listar_ahorros():
    activos = request.args.get('activos', 'true') == 'true'
    ahorros = Ahorro.query.filter_by(
        usuario_id=current_user.id,
        activo=activos
    ).order_by(Ahorro.fecha_creacion.desc()).all()
    return render_template('ahorros/listar.html', ahorros=ahorros, activos=activos)

@ahorros_bp.route('/ahorros/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_ahorro():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descripcion = request.form.get('descripcion')
        monto = request.form.get('monto')
        frecuencia = request.form.get('frecuencia', 'mensual')
        fecha_inicio = request.form.get('fecha_inicio')
        fecha_fin = request.form.get('fecha_fin')
        
        if not all([titulo, monto, fecha_inicio]):
            flash('Por favor completa todos los campos obligatorios.', 'error')
            fecha_actual = date.today().strftime('%Y-%m-%d')
            return render_template('ahorros/nuevo.html', fecha_actual=fecha_actual)
        
        try:
            ahorro = Ahorro(
                usuario_id=current_user.id,
                titulo=titulo,
                descripcion=descripcion or '',
                monto=float(monto),
                frecuencia=frecuencia,
                fecha_inicio=datetime.strptime(fecha_inicio, '%Y-%m-%d').date(),
                fecha_fin=datetime.strptime(fecha_fin, '%Y-%m-%d').date() if fecha_fin else None
            )
            db.session.add(ahorro)
            db.session.commit()
            flash('Ahorro programado creado exitosamente.', 'success')
            return redirect(url_for('ahorros.listar_ahorros'))
        except Exception as e:
            flash(f'Error al crear el ahorro: {str(e)}', 'error')
            db.session.rollback()
    
    fecha_actual = date.today().strftime('%Y-%m-%d')
    return render_template('ahorros/nuevo.html', fecha_actual=fecha_actual)

@ahorros_bp.route('/ahorros/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_ahorro(id):
    ahorro = Ahorro.query.get_or_404(id)
    
    if ahorro.usuario_id != current_user.id:
        flash('No tienes permiso para editar este ahorro.', 'error')
        return redirect(url_for('ahorros.listar_ahorros'))
    
    if request.method == 'POST':
        ahorro.titulo = request.form.get('titulo')
        ahorro.descripcion = request.form.get('descripcion')
        ahorro.monto = float(request.form.get('monto'))
        ahorro.frecuencia = request.form.get('frecuencia', 'mensual')
        ahorro.fecha_inicio = datetime.strptime(request.form.get('fecha_inicio'), '%Y-%m-%d').date()
        fecha_fin = request.form.get('fecha_fin')
        ahorro.fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date() if fecha_fin else None
        
        try:
            db.session.commit()
            flash('Ahorro actualizado exitosamente.', 'success')
            return redirect(url_for('ahorros.listar_ahorros'))
        except Exception as e:
            flash(f'Error al actualizar el ahorro: {str(e)}', 'error')
            db.session.rollback()
    
    return render_template('ahorros/editar.html', ahorro=ahorro)

@ahorros_bp.route('/ahorros/<int:id>/toggle', methods=['POST'])
@login_required
def toggle_ahorro(id):
    ahorro = Ahorro.query.get_or_404(id)
    
    if ahorro.usuario_id != current_user.id:
        flash('No tienes permiso para modificar este ahorro.', 'error')
        return redirect(url_for('ahorros.listar_ahorros'))
    
    ahorro.activo = not ahorro.activo
    
    try:
        db.session.commit()
        estado = 'activado' if ahorro.activo else 'desactivado'
        flash(f'Ahorro {estado} exitosamente.', 'success')
    except Exception as e:
        flash(f'Error al modificar el ahorro: {str(e)}', 'error')
        db.session.rollback()
    
    return redirect(url_for('ahorros.listar_ahorros'))

@ahorros_bp.route('/ahorros/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar_ahorro(id):
    ahorro = Ahorro.query.get_or_404(id)
    
    if ahorro.usuario_id != current_user.id:
        flash('No tienes permiso para eliminar este ahorro.', 'error')
        return redirect(url_for('ahorros.listar_ahorros'))
    
    try:
        db.session.delete(ahorro)
        db.session.commit()
        flash('Ahorro eliminado exitosamente.', 'success')
    except Exception as e:
        flash(f'Error al eliminar el ahorro: {str(e)}', 'error')
        db.session.rollback()
    
    return redirect(url_for('ahorros.listar_ahorros'))

