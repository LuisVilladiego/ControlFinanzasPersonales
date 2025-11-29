from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import Meta
from database import db
from datetime import datetime, date

metas_bp = Blueprint('metas', __name__)

@metas_bp.route('/metas')
@login_required
def listar_metas():
    completadas = request.args.get('completadas', 'false') == 'true'
    metas = Meta.query.filter_by(
        usuario_id=current_user.id,
        completada=completadas
    ).order_by(Meta.fecha_limite.asc()).all()
    return render_template('metas/listar.html', metas=metas, completadas=completadas)

@metas_bp.route('/metas/nueva', methods=['GET', 'POST'])
@login_required
def nueva_meta():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descripcion = request.form.get('descripcion')
        monto_objetivo = request.form.get('monto_objetivo')
        fecha_limite = request.form.get('fecha_limite')
        
        if not all([titulo, monto_objetivo, fecha_limite]):
            flash('Por favor completa todos los campos obligatorios.', 'error')
            return render_template('metas/nueva.html')
        
        try:
            meta = Meta(
                usuario_id=current_user.id,
                titulo=titulo,
                descripcion=descripcion or '',
                monto_objetivo=float(monto_objetivo),
                fecha_limite=datetime.strptime(fecha_limite, '%Y-%m-%d').date()
            )
            db.session.add(meta)
            db.session.commit()
            flash('Meta creada exitosamente.', 'success')
            return redirect(url_for('metas.listar_metas'))
        except Exception as e:
            flash(f'Error al crear la meta: {str(e)}', 'error')
            db.session.rollback()
    
    return render_template('metas/nueva.html')

@metas_bp.route('/metas/<int:id>')
@login_required
def ver_meta(id):
    meta = Meta.query.get_or_404(id)
    
    if meta.usuario_id != current_user.id:
        flash('No tienes permiso para ver esta meta.', 'error')
        return redirect(url_for('metas.listar_metas'))
    
    return render_template('metas/ver.html', meta=meta)

@metas_bp.route('/metas/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_meta(id):
    meta = Meta.query.get_or_404(id)
    
    if meta.usuario_id != current_user.id:
        flash('No tienes permiso para editar esta meta.', 'error')
        return redirect(url_for('metas.listar_metas'))
    
    if request.method == 'POST':
        meta.titulo = request.form.get('titulo')
        meta.descripcion = request.form.get('descripcion')
        meta.monto_objetivo = float(request.form.get('monto_objetivo'))
        meta.fecha_limite = datetime.strptime(request.form.get('fecha_limite'), '%Y-%m-%d').date()
        
        try:
            db.session.commit()
            flash('Meta actualizada exitosamente.', 'success')
            return redirect(url_for('metas.ver_meta', id=id))
        except Exception as e:
            flash(f'Error al actualizar la meta: {str(e)}', 'error')
            db.session.rollback()
    
    return render_template('metas/editar.html', meta=meta)

@metas_bp.route('/metas/<int:id>/agregar', methods=['POST'])
@login_required
def agregar_monto_meta(id):
    meta = Meta.query.get_or_404(id)
    
    if meta.usuario_id != current_user.id:
        flash('No tienes permiso para modificar esta meta.', 'error')
        return redirect(url_for('metas.listar_metas'))
    
    from decimal import Decimal
    monto = Decimal(str(request.form.get('monto', 0)))
    
    if monto > 0:
        meta.monto_actual += monto
        if meta.monto_actual >= meta.monto_objetivo:
            meta.completada = True
            meta.monto_actual = meta.monto_objetivo
        
        try:
            db.session.commit()
            flash(f'Se agregaron ${float(monto):.2f} a la meta.', 'success')
        except Exception as e:
            flash(f'Error al actualizar la meta: {str(e)}', 'error')
            db.session.rollback()
    
    return redirect(url_for('metas.ver_meta', id=id))

@metas_bp.route('/metas/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar_meta(id):
    meta = Meta.query.get_or_404(id)
    
    if meta.usuario_id != current_user.id:
        flash('No tienes permiso para eliminar esta meta.', 'error')
        return redirect(url_for('metas.listar_metas'))
    
    try:
        db.session.delete(meta)
        db.session.commit()
        flash('Meta eliminada exitosamente.', 'success')
    except Exception as e:
        flash(f'Error al eliminar la meta: {str(e)}', 'error')
        db.session.rollback()
    
    return redirect(url_for('metas.listar_metas'))

