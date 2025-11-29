from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from models import Ingreso, Egreso, Meta, Ahorro, Recordatorio, DeudaFija
from database import db
from datetime import datetime, date, timedelta
from sqlalchemy import func, extract

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    # Estadísticas del mes actual
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
    
    # Últimos ingresos y egresos
    ultimos_ingresos = Ingreso.query.filter_by(usuario_id=current_user.id)\
        .order_by(Ingreso.fecha.desc()).limit(5).all()
    ultimos_egresos = Egreso.query.filter_by(usuario_id=current_user.id)\
        .order_by(Egreso.fecha.desc()).limit(5).all()
    
    # Metas activas
    metas_activas = Meta.query.filter_by(
        usuario_id=current_user.id,
        completada=False
    ).order_by(Meta.fecha_limite.asc()).limit(5).all()
    
    # Recordatorios pendientes
    recordatorios_pendientes = Recordatorio.query.filter_by(
        usuario_id=current_user.id,
        enviado=False
    ).filter(Recordatorio.fecha_pago >= hoy)\
     .order_by(Recordatorio.fecha_pago.asc()).limit(5).all()
    
    # Deudas fijas pendientes
    deudas_pendientes = DeudaFija.query.filter_by(
        usuario_id=current_user.id,
        activa=True,
        pagada_este_mes=False
    ).all()
    
    # Actualizar estado de pagos mensuales
    for deuda in deudas_pendientes:
        if deuda.pagada_este_mes and deuda.fecha_ultimo_pago:
            if deuda.fecha_ultimo_pago.year != hoy.year or deuda.fecha_ultimo_pago.month != hoy.month:
                deuda.pagada_este_mes = False
                db.session.commit()
    
    # Calcular próximas fechas de pago para deudas
    deudas_con_fecha = []
    for deuda in deudas_pendientes:
        fecha_pago_mes = date(hoy.year, hoy.month, min(deuda.dia_pago, 28))
        if fecha_pago_mes < hoy:
            if hoy.month == 12:
                fecha_pago_mes = date(hoy.year + 1, 1, min(deuda.dia_pago, 28))
            else:
                fecha_pago_mes = date(hoy.year, hoy.month + 1, min(deuda.dia_pago, 28))
        deudas_con_fecha.append({
            'deuda': deuda,
            'fecha_pago': fecha_pago_mes,
            'dias_restantes': (fecha_pago_mes - hoy).days
        })
    
    # Ordenar por fecha de pago
    deudas_con_fecha.sort(key=lambda x: x['fecha_pago'])
    deudas_pendientes_ordenadas = [d['deuda'] for d in deudas_con_fecha[:5]]
    
    # Alertas de metas próximas a vencer
    alertas_metas = []
    for meta in metas_activas:
        dias_restantes = (meta.fecha_limite - hoy).days
        if dias_restantes <= 30 and not meta.completada:
            alertas_metas.append({
                'meta': meta,
                'dias_restantes': dias_restantes,
                'porcentaje': meta.porcentaje_completado()
            })
    
    # Datos para gráficos (últimos 6 meses)
    meses_datos = []
    ingresos_grafico = []
    egresos_grafico = []
    
    for i in range(5, -1, -1):
        mes_fecha = date(hoy.year, hoy.month, 1) - timedelta(days=30*i)
        mes_siguiente = date(mes_fecha.year, mes_fecha.month + 1, 1) if mes_fecha.month < 12 else date(mes_fecha.year + 1, 1, 1)
        
        ing = db.session.query(func.sum(Ingreso.monto)).filter(
            Ingreso.usuario_id == current_user.id,
            Ingreso.fecha >= mes_fecha,
            Ingreso.fecha < mes_siguiente
        ).scalar() or 0
        
        egr = db.session.query(func.sum(Egreso.monto)).filter(
            Egreso.usuario_id == current_user.id,
            Egreso.fecha >= mes_fecha,
            Egreso.fecha < mes_siguiente
        ).scalar() or 0
        
        meses_datos.append(mes_fecha.strftime('%b %Y'))
        ingresos_grafico.append(float(ing))
        egresos_grafico.append(float(egr))
    
    # Ingresos por categoría (mes actual)
    ingresos_categoria = db.session.query(
        Ingreso.categoria,
        func.sum(Ingreso.monto).label('total')
    ).filter(
        Ingreso.usuario_id == current_user.id,
        Ingreso.fecha >= inicio_mes
    ).group_by(Ingreso.categoria).all()
    
    # Egresos por categoría (mes actual)
    egresos_categoria = db.session.query(
        Egreso.categoria,
        func.sum(Egreso.monto).label('total')
    ).filter(
        Egreso.usuario_id == current_user.id,
        Egreso.fecha >= inicio_mes
    ).group_by(Egreso.categoria).all()
    
    return render_template('dashboard.html',
                         ingresos_mes=ingresos_mes,
                         egresos_mes=egresos_mes,
                         balance_mes=balance_mes,
                         ultimos_ingresos=ultimos_ingresos,
                         ultimos_egresos=ultimos_egresos,
                         metas_activas=metas_activas,
                         recordatorios_pendientes=recordatorios_pendientes,
                         meses_datos=meses_datos,
                         ingresos_grafico=ingresos_grafico,
                         egresos_grafico=egresos_grafico,
                         ingresos_categoria=ingresos_categoria,
                         egresos_categoria=egresos_categoria,
                         alertas_metas=alertas_metas,
                         deudas_pendientes=deudas_pendientes_ordenadas,
                         deudas_con_fecha=deudas_con_fecha[:5])

