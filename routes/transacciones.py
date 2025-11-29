from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import Ingreso, Egreso
from database import db
from datetime import datetime, date

transacciones_bp = Blueprint('transacciones', __name__)

@transacciones_bp.route('/ingresos')
@login_required
def listar_ingresos():
    page = request.args.get('page', 1, type=int)
    ingresos = Ingreso.query.filter_by(usuario_id=current_user.id)\
        .order_by(Ingreso.fecha.desc())\
        .paginate(page=page, per_page=10, error_out=False)
    return render_template('transacciones/ingresos.html', ingresos=ingresos)

@transacciones_bp.route('/ingresos/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_ingreso():
    if request.method == 'POST':
        monto = request.form.get('monto')
        descripcion = request.form.get('descripcion')
        categoria = request.form.get('categoria')
        fecha = request.form.get('fecha')
        
        if not all([monto, descripcion, categoria, fecha]):
            flash('Por favor completa todos los campos.', 'error')
            fecha_actual = date.today().strftime('%Y-%m-%d')
            return render_template('transacciones/nuevo_ingreso.html', fecha_actual=fecha_actual)
        
        try:
            ingreso = Ingreso(
                usuario_id=current_user.id,
                monto=float(monto),
                descripcion=descripcion,
                categoria=categoria,
                fecha=datetime.strptime(fecha, '%Y-%m-%d').date()
            )
            db.session.add(ingreso)
            db.session.commit()
            flash('Ingreso registrado exitosamente.', 'success')
            return redirect(url_for('transacciones.listar_ingresos'))
        except Exception as e:
            flash(f'Error al registrar el ingreso: {str(e)}', 'error')
            db.session.rollback()
    
    fecha_actual = date.today().strftime('%Y-%m-%d')
    return render_template('transacciones/nuevo_ingreso.html', fecha_actual=fecha_actual)

@transacciones_bp.route('/ingresos/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_ingreso(id):
    ingreso = Ingreso.query.get_or_404(id)
    
    if ingreso.usuario_id != current_user.id:
        flash('No tienes permiso para editar este ingreso.', 'error')
        return redirect(url_for('transacciones.listar_ingresos'))
    
    if request.method == 'POST':
        ingreso.monto = float(request.form.get('monto'))
        ingreso.descripcion = request.form.get('descripcion')
        ingreso.categoria = request.form.get('categoria')
        ingreso.fecha = datetime.strptime(request.form.get('fecha'), '%Y-%m-%d').date()
        
        try:
            db.session.commit()
            flash('Ingreso actualizado exitosamente.', 'success')
            return redirect(url_for('transacciones.listar_ingresos'))
        except Exception as e:
            flash(f'Error al actualizar el ingreso: {str(e)}', 'error')
            db.session.rollback()
    
    return render_template('transacciones/editar_ingreso.html', ingreso=ingreso)

@transacciones_bp.route('/ingresos/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar_ingreso(id):
    ingreso = Ingreso.query.get_or_404(id)
    
    if ingreso.usuario_id != current_user.id:
        flash('No tienes permiso para eliminar este ingreso.', 'error')
        return redirect(url_for('transacciones.listar_ingresos'))
    
    try:
        db.session.delete(ingreso)
        db.session.commit()
        flash('Ingreso eliminado exitosamente.', 'success')
    except Exception as e:
        flash(f'Error al eliminar el ingreso: {str(e)}', 'error')
        db.session.rollback()
    
    return redirect(url_for('transacciones.listar_ingresos'))

@transacciones_bp.route('/egresos')
@login_required
def listar_egresos():
    page = request.args.get('page', 1, type=int)
    egresos = Egreso.query.filter_by(usuario_id=current_user.id)\
        .order_by(Egreso.fecha.desc())\
        .paginate(page=page, per_page=10, error_out=False)
    return render_template('transacciones/egresos.html', egresos=egresos)

@transacciones_bp.route('/egresos/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_egreso():
    if request.method == 'POST':
        monto = request.form.get('monto')
        descripcion = request.form.get('descripcion')
        categoria = request.form.get('categoria')
        fecha = request.form.get('fecha')
        
        if not all([monto, descripcion, categoria, fecha]):
            flash('Por favor completa todos los campos.', 'error')
            fecha_actual = date.today().strftime('%Y-%m-%d')
            return render_template('transacciones/nuevo_egreso.html', fecha_actual=fecha_actual)
        
        try:
            egreso = Egreso(
                usuario_id=current_user.id,
                monto=float(monto),
                descripcion=descripcion,
                categoria=categoria,
                fecha=datetime.strptime(fecha, '%Y-%m-%d').date()
            )
            db.session.add(egreso)
            db.session.commit()
            flash('Egreso registrado exitosamente.', 'success')
            return redirect(url_for('transacciones.listar_egresos'))
        except Exception as e:
            flash(f'Error al registrar el egreso: {str(e)}', 'error')
            db.session.rollback()
    
    fecha_actual = date.today().strftime('%Y-%m-%d')
    return render_template('transacciones/nuevo_egreso.html', fecha_actual=fecha_actual)

@transacciones_bp.route('/egresos/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_egreso(id):
    egreso = Egreso.query.get_or_404(id)
    
    if egreso.usuario_id != current_user.id:
        flash('No tienes permiso para editar este egreso.', 'error')
        return redirect(url_for('transacciones.listar_egresos'))
    
    if request.method == 'POST':
        egreso.monto = float(request.form.get('monto'))
        egreso.descripcion = request.form.get('descripcion')
        egreso.categoria = request.form.get('categoria')
        egreso.fecha = datetime.strptime(request.form.get('fecha'), '%Y-%m-%d').date()
        
        try:
            db.session.commit()
            flash('Egreso actualizado exitosamente.', 'success')
            return redirect(url_for('transacciones.listar_egresos'))
        except Exception as e:
            flash(f'Error al actualizar el egreso: {str(e)}', 'error')
            db.session.rollback()
    
    return render_template('transacciones/editar_egreso.html', egreso=egreso)

@transacciones_bp.route('/egresos/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar_egreso(id):
    egreso = Egreso.query.get_or_404(id)
    
    if egreso.usuario_id != current_user.id:
        flash('No tienes permiso para eliminar este egreso.', 'error')
        return redirect(url_for('transacciones.listar_egresos'))
    
    try:
        db.session.delete(egreso)
        db.session.commit()
        flash('Egreso eliminado exitosamente.', 'success')
    except Exception as e:
        flash(f'Error al eliminar el egreso: {str(e)}', 'error')
        db.session.rollback()
    
    return redirect(url_for('transacciones.listar_egresos'))

