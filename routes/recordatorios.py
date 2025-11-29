from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import Recordatorio
from database import db
from datetime import datetime, date

recordatorios_bp = Blueprint('recordatorios', __name__)

@recordatorios_bp.route('/recordatorios')
@login_required
def listar_recordatorios():
    enviados = request.args.get('enviados', 'false') == 'true'
    recordatorios = Recordatorio.query.filter_by(
        usuario_id=current_user.id,
        enviado=enviados
    ).order_by(Recordatorio.fecha_pago.asc()).all()
    return render_template('recordatorios/listar.html', recordatorios=recordatorios, enviados=enviados)

@recordatorios_bp.route('/recordatorios/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_recordatorio():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descripcion = request.form.get('descripcion')
        monto = request.form.get('monto')
        fecha_pago = request.form.get('fecha_pago')
        fecha_recordatorio = request.form.get('fecha_recordatorio')
        
        if not all([titulo, monto, fecha_pago, fecha_recordatorio]):
            flash('Por favor completa todos los campos obligatorios.', 'error')
            return render_template('recordatorios/nuevo.html')
        
        try:
            recordatorio = Recordatorio(
                usuario_id=current_user.id,
                titulo=titulo,
                descripcion=descripcion or '',
                monto=float(monto),
                fecha_pago=datetime.strptime(fecha_pago, '%Y-%m-%d').date(),
                fecha_recordatorio=datetime.strptime(fecha_recordatorio, '%Y-%m-%d').date()
            )
            db.session.add(recordatorio)
            db.session.commit()
            flash('Recordatorio creado exitosamente.', 'success')
            return redirect(url_for('recordatorios.listar_recordatorios'))
        except Exception as e:
            flash(f'Error al crear el recordatorio: {str(e)}', 'error')
            db.session.rollback()
    
    return render_template('recordatorios/nuevo.html')

@recordatorios_bp.route('/recordatorios/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_recordatorio(id):
    recordatorio = Recordatorio.query.get_or_404(id)
    
    if recordatorio.usuario_id != current_user.id:
        flash('No tienes permiso para editar este recordatorio.', 'error')
        return redirect(url_for('recordatorios.listar_recordatorios'))
    
    if request.method == 'POST':
        recordatorio.titulo = request.form.get('titulo')
        recordatorio.descripcion = request.form.get('descripcion')
        recordatorio.monto = float(request.form.get('monto'))
        recordatorio.fecha_pago = datetime.strptime(request.form.get('fecha_pago'), '%Y-%m-%d').date()
        recordatorio.fecha_recordatorio = datetime.strptime(request.form.get('fecha_recordatorio'), '%Y-%m-%d').date()
        
        try:
            db.session.commit()
            flash('Recordatorio actualizado exitosamente.', 'success')
            return redirect(url_for('recordatorios.listar_recordatorios'))
        except Exception as e:
            flash(f'Error al actualizar el recordatorio: {str(e)}', 'error')
            db.session.rollback()
    
    return render_template('recordatorios/editar.html', recordatorio=recordatorio)

@recordatorios_bp.route('/recordatorios/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar_recordatorio(id):
    recordatorio = Recordatorio.query.get_or_404(id)
    
    if recordatorio.usuario_id != current_user.id:
        flash('No tienes permiso para eliminar este recordatorio.', 'error')
        return redirect(url_for('recordatorios.listar_recordatorios'))
    
    try:
        db.session.delete(recordatorio)
        db.session.commit()
        flash('Recordatorio eliminado exitosamente.', 'success')
    except Exception as e:
        flash(f'Error al eliminar el recordatorio: {str(e)}', 'error')
        db.session.rollback()
    
    return redirect(url_for('recordatorios.listar_recordatorios'))

