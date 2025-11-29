"""
Rutas para gestión de deudas fijas.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import DeudaFija
from database import db
from datetime import datetime, date, timedelta
from services.validators import validate_monto, validate_texto, ValidationError

deudas_bp = Blueprint('deudas', __name__)

@deudas_bp.route('/deudas')
@login_required
def listar_deudas():
    """Lista todas las deudas fijas del usuario."""
    activas = request.args.get('activas', 'true') == 'true'
    deudas = DeudaFija.query.filter_by(
        usuario_id=current_user.id,
        activa=activas
    ).order_by(DeudaFija.dia_pago.asc()).all()
    
    # Actualizar estado de pagos mensuales
    hoy = date.today()
    deudas_con_info = []
    
    for deuda in deudas:
        if deuda.pagada_este_mes and deuda.fecha_ultimo_pago:
            # Si cambió el mes, resetear el estado de pago
            if deuda.fecha_ultimo_pago.year != hoy.year or deuda.fecha_ultimo_pago.month != hoy.month:
                deuda.pagada_este_mes = False
                db.session.commit()
        
        # Calcular fecha de pago del mes actual
        fecha_pago_mes = date(hoy.year, hoy.month, min(deuda.dia_pago, 28))
        if fecha_pago_mes < hoy:
            # Si ya pasó, usar el próximo mes
            if hoy.month == 12:
                fecha_pago_mes = date(hoy.year + 1, 1, min(deuda.dia_pago, 28))
            else:
                fecha_pago_mes = date(hoy.year, hoy.month + 1, min(deuda.dia_pago, 28))
        
        dias_restantes = (fecha_pago_mes - hoy).days
        
        deudas_con_info.append({
            'deuda': deuda,
            'fecha_pago': fecha_pago_mes,
            'dias_restantes': dias_restantes
        })
    
    return render_template('deudas/listar.html', deudas_con_info=deudas_con_info, activas=activas)

@deudas_bp.route('/deudas/nueva', methods=['GET', 'POST'])
@login_required
def nueva_deuda():
    """Crea una nueva deuda fija."""
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descripcion = request.form.get('descripcion')
        monto = request.form.get('monto')
        dia_pago = request.form.get('dia_pago')
        
        if not all([titulo, monto, dia_pago]):
            flash('Por favor completa todos los campos obligatorios.', 'error')
            return render_template('deudas/nueva.html')
        
        try:
            # Validar monto
            es_valido, error, monto_decimal = validate_monto(monto)
            if not es_valido:
                flash(error, 'error')
                return render_template('deudas/nueva.html')
            
            # Validar día de pago
            dia_pago_int = int(dia_pago)
            if dia_pago_int < 1 or dia_pago_int > 31:
                flash('El día de pago debe estar entre 1 y 31.', 'error')
                return render_template('deudas/nueva.html')
            
            # Calcular fecha de pago inicial
            hoy = date.today()
            fecha_pago = date(hoy.year, hoy.month, min(dia_pago_int, 28))
            if fecha_pago < hoy:
                # Si la fecha ya pasó, usar el próximo mes
                if hoy.month == 12:
                    fecha_pago = date(hoy.year + 1, 1, min(dia_pago_int, 28))
                else:
                    fecha_pago = date(hoy.year, hoy.month + 1, min(dia_pago_int, 28))
            
            deuda = DeudaFija(
                usuario_id=current_user.id,
                titulo=titulo,
                descripcion=descripcion or '',
                monto=monto_decimal,
                fecha_pago=fecha_pago,
                dia_pago=dia_pago_int,
                activa=True,
                pagada_este_mes=False
            )
            
            db.session.add(deuda)
            db.session.commit()
            flash('Deuda fija creada exitosamente.', 'success')
            return redirect(url_for('deudas.listar_deudas'))
        except ValueError:
            flash('El día de pago debe ser un número válido.', 'error')
        except Exception as e:
            flash(f'Error al crear la deuda: {str(e)}', 'error')
            db.session.rollback()
    
    return render_template('deudas/nueva.html')

@deudas_bp.route('/deudas/<int:id>/marcar_pagada', methods=['POST'])
@login_required
def marcar_pagada(id):
    """Marca una deuda como pagada."""
    deuda = DeudaFija.query.get_or_404(id)
    
    if deuda.usuario_id != current_user.id:
        flash('No tienes permiso para modificar esta deuda.', 'error')
        return redirect(url_for('deudas.listar_deudas'))
    
    try:
        deuda.pagada_este_mes = True
        deuda.fecha_ultimo_pago = date.today()
        
        # Crear un egreso automático cuando se marca como pagada
        from models import Egreso
        egreso = Egreso(
            usuario_id=current_user.id,
            monto=deuda.monto,
            descripcion=f'Pago de deuda: {deuda.titulo}',
            categoria='Deudas',
            fecha=date.today()
        )
        db.session.add(egreso)
        db.session.commit()
        
        flash(f'Deuda "{deuda.titulo}" marcada como pagada. Egreso registrado automáticamente.', 'success')
    except Exception as e:
        flash(f'Error al marcar la deuda como pagada: {str(e)}', 'error')
        db.session.rollback()
    
    return redirect(url_for('deudas.listar_deudas'))

@deudas_bp.route('/deudas/<int:id>/desmarcar_pagada', methods=['POST'])
@login_required
def desmarcar_pagada(id):
    """Desmarca una deuda como pagada."""
    deuda = DeudaFija.query.get_or_404(id)
    
    if deuda.usuario_id != current_user.id:
        flash('No tienes permiso para modificar esta deuda.', 'error')
        return redirect(url_for('deudas.listar_deudas'))
    
    try:
        deuda.pagada_este_mes = False
        db.session.commit()
        flash(f'Deuda "{deuda.titulo}" desmarcada como pagada.', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        db.session.rollback()
    
    return redirect(url_for('deudas.listar_deudas'))

@deudas_bp.route('/deudas/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_deuda(id):
    """Edita una deuda fija existente."""
    deuda = DeudaFija.query.get_or_404(id)
    
    if deuda.usuario_id != current_user.id:
        flash('No tienes permiso para editar esta deuda.', 'error')
        return redirect(url_for('deudas.listar_deudas'))
    
    if request.method == 'POST':
        deuda.titulo = request.form.get('titulo')
        deuda.descripcion = request.form.get('descripcion')
        monto = request.form.get('monto')
        dia_pago = request.form.get('dia_pago')
        
        try:
            es_valido, error, monto_decimal = validate_monto(monto)
            if not es_valido:
                flash(error, 'error')
                return render_template('deudas/editar.html', deuda=deuda)
            
            deuda.monto = monto_decimal
            deuda.dia_pago = int(dia_pago)
            
            # Actualizar fecha de pago
            hoy = date.today()
            fecha_pago = date(hoy.year, hoy.month, min(deuda.dia_pago, 28))
            if fecha_pago < hoy:
                if hoy.month == 12:
                    fecha_pago = date(hoy.year + 1, 1, min(deuda.dia_pago, 28))
                else:
                    fecha_pago = date(hoy.year, hoy.month + 1, min(deuda.dia_pago, 28))
            deuda.fecha_pago = fecha_pago
            
            db.session.commit()
            flash('Deuda actualizada exitosamente.', 'success')
            return redirect(url_for('deudas.listar_deudas'))
        except Exception as e:
            flash(f'Error al actualizar la deuda: {str(e)}', 'error')
            db.session.rollback()
    
    return render_template('deudas/editar.html', deuda=deuda)

@deudas_bp.route('/deudas/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar_deuda(id):
    """Elimina una deuda fija."""
    deuda = DeudaFija.query.get_or_404(id)
    
    if deuda.usuario_id != current_user.id:
        flash('No tienes permiso para eliminar esta deuda.', 'error')
        return redirect(url_for('deudas.listar_deudas'))
    
    try:
        db.session.delete(deuda)
        db.session.commit()
        flash('Deuda eliminada exitosamente.', 'success')
    except Exception as e:
        flash(f'Error al eliminar la deuda: {str(e)}', 'error')
        db.session.rollback()
    
    return redirect(url_for('deudas.listar_deudas'))

@deudas_bp.route('/deudas/<int:id>/toggle', methods=['POST'])
@login_required
def toggle_deuda(id):
    """Activa/desactiva una deuda."""
    deuda = DeudaFija.query.get_or_404(id)
    
    if deuda.usuario_id != current_user.id:
        flash('No tienes permiso para modificar esta deuda.', 'error')
        return redirect(url_for('deudas.listar_deudas'))
    
    deuda.activa = not deuda.activa
    
    try:
        db.session.commit()
        estado = 'activada' if deuda.activa else 'desactivada'
        flash(f'Deuda {estado} exitosamente.', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        db.session.rollback()
    
    return redirect(url_for('deudas.listar_deudas'))

