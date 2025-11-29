"""
Rutas para estrategias de pago de deudas.
Implementa métodos como Avalancha y Bola de Nieve para optimizar el pago de deudas.
"""
from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from models import DeudaFija
from database import db
from datetime import date
from decimal import Decimal

estrategias_bp = Blueprint('estrategias', __name__)

def calcular_interes_mensual(saldo, tasa_anual):
    """Calcula el interés mensual basado en el saldo y la tasa anual."""
    if tasa_anual <= 0:
        return Decimal('0')
    tasa_mensual = Decimal(str(tasa_anual)) / Decimal('12') / Decimal('100')
    return saldo * tasa_mensual

def metodo_avalancha(deudas_info, pago_extra_mensual):
    """
    Método Avalancha: Pagar primero la deuda con mayor tasa de interés.
    Minimiza el total de intereses pagados.
    """
    # Ordenar deudas por tasa de interés descendente
    deudas_ordenadas = sorted(deudas_info, key=lambda x: x['tasa_interes'], reverse=True)
    
    meses = 0
    total_intereses = Decimal('0')
    historial = []
    deudas_actuales = [{
        'id': d['id'],
        'saldo': Decimal(str(d['saldo_pendiente'])),
        'pago_minimo': Decimal(str(d['pago_minimo'])),
        'tasa_interes': Decimal(str(d['tasa_interes'])),
        'nombre': d['nombre']
    } for d in deudas_ordenadas]
    
    while any(d['saldo'] > 0 for d in deudas_actuales):
        meses += 1
        mes_intereses = Decimal('0')
        pago_total_mes = Decimal('0')
        
        # Calcular intereses y pagos mínimos
        for deuda in deudas_actuales:
            if deuda['saldo'] > 0:
                interes = calcular_interes_mensual(deuda['saldo'], float(deuda['tasa_interes']))
                deuda['saldo'] += interes
                mes_intereses += interes
                total_intereses += interes
                
                # Pago mínimo
                pago = min(deuda['pago_minimo'], deuda['saldo'])
                deuda['saldo'] -= pago
                pago_total_mes += pago
        
        # Aplicar pago extra a la deuda con mayor tasa de interés (que aún tenga saldo)
        deudas_pendientes = [d for d in deudas_actuales if d['saldo'] > 0]
        if deudas_pendientes and pago_extra_mensual > 0:
            deuda_activa = max(deudas_pendientes, key=lambda x: x['tasa_interes'])
            pago_extra = min(Decimal(str(pago_extra_mensual)), deuda_activa['saldo'])
            deuda_activa['saldo'] -= pago_extra
            pago_total_mes += pago_extra
        
        # Guardar estado del mes
        if meses <= 12 or any(d['saldo'] > 0 for d in deudas_actuales):
            historial.append({
                'mes': meses,
                'total_intereses': float(mes_intereses),
                'pago_total': float(pago_total_mes),
                'saldos': {d['nombre']: float(d['saldo']) for d in deudas_actuales if d['saldo'] > 0}
            })
        
        # Evitar bucle infinito
        if meses > 600:  # 50 años máximo
            break
    
    return {
        'meses': meses,
        'total_intereses': float(total_intereses),
        'historial': historial[:24]  # Primeros 24 meses
    }

def metodo_bola_nieve(deudas_info, pago_extra_mensual):
    """
    Método Bola de Nieve: Pagar primero la deuda más pequeña.
    Proporciona motivación psicológica al ver deudas eliminadas rápidamente.
    """
    # Ordenar deudas por saldo pendiente ascendente
    deudas_ordenadas = sorted(deudas_info, key=lambda x: x['saldo_pendiente'])
    
    meses = 0
    total_intereses = Decimal('0')
    historial = []
    deudas_actuales = [{
        'id': d['id'],
        'saldo': Decimal(str(d['saldo_pendiente'])),
        'pago_minimo': Decimal(str(d['pago_minimo'])),
        'tasa_interes': Decimal(str(d['tasa_interes'])),
        'nombre': d['nombre']
    } for d in deudas_ordenadas]
    
    while any(d['saldo'] > 0 for d in deudas_actuales):
        meses += 1
        mes_intereses = Decimal('0')
        pago_total_mes = Decimal('0')
        
        # Calcular intereses y pagos mínimos
        for deuda in deudas_actuales:
            if deuda['saldo'] > 0:
                interes = calcular_interes_mensual(deuda['saldo'], float(deuda['tasa_interes']))
                deuda['saldo'] += interes
                mes_intereses += interes
                total_intereses += interes
                
                # Pago mínimo
                pago = min(deuda['pago_minimo'], deuda['saldo'])
                deuda['saldo'] -= pago
                pago_total_mes += pago
        
        # Aplicar pago extra a la deuda más pequeña
        deudas_pendientes = [d for d in deudas_actuales if d['saldo'] > 0]
        if deudas_pendientes and pago_extra_mensual > 0:
            deuda_activa = min(deudas_pendientes, key=lambda x: x['saldo'])
            pago_extra = min(Decimal(str(pago_extra_mensual)), deuda_activa['saldo'])
            deuda_activa['saldo'] -= pago_extra
            pago_total_mes += pago_extra
        
        # Guardar estado del mes
        if meses <= 12 or any(d['saldo'] > 0 for d in deudas_actuales):
            historial.append({
                'mes': meses,
                'total_intereses': float(mes_intereses),
                'pago_total': float(pago_total_mes),
                'saldos': {d['nombre']: float(d['saldo']) for d in deudas_actuales if d['saldo'] > 0}
            })
        
        # Evitar bucle infinito
        if meses > 600:  # 50 años máximo
            break
    
    return {
        'meses': meses,
        'total_intereses': float(total_intereses),
        'historial': historial[:24]  # Primeros 24 meses
    }

@estrategias_bp.route('/estrategias-deuda')
@login_required
def estrategias_deuda():
    """Muestra la página de estrategias de pago de deudas."""
    deudas = DeudaFija.query.filter_by(
        usuario_id=current_user.id,
        activa=True
    ).all()
    
    resultados = None
    deudas_info = []
    
    if request.method == 'POST':
        # Obtener datos del formulario
        pago_extra = request.form.get('pago_extra', '0')
        
        try:
            pago_extra_decimal = Decimal(pago_extra) if pago_extra else Decimal('0')
            
            # Recopilar información de deudas del formulario
            for deuda in deudas:
                saldo_key = f'saldo_{deuda.id}'
                tasa_key = f'tasa_{deuda.id}'
                pago_min_key = f'pago_min_{deuda.id}'
                
                saldo = request.form.get(saldo_key, '0')
                tasa = request.form.get(tasa_key, '0')
                pago_min = request.form.get(pago_min_key, str(deuda.monto))
                
                try:
                    saldo_decimal = Decimal(saldo) if saldo else Decimal('0')
                    tasa_decimal = Decimal(tasa) if tasa else Decimal('0')
                    pago_min_decimal = Decimal(pago_min) if pago_min else Decimal(str(deuda.monto))
                    
                    if saldo_decimal > 0:
                        deudas_info.append({
                            'id': deuda.id,
                            'nombre': deuda.titulo,
                            'saldo_pendiente': float(saldo_decimal),
                            'tasa_interes': float(tasa_decimal),
                            'pago_minimo': float(pago_min_decimal)
                        })
                except (ValueError, TypeError):
                    continue
            
            if not deudas_info:
                flash('Debes ingresar al menos una deuda con saldo pendiente mayor a 0.', 'error')
            else:
                # Calcular ambas estrategias
                resultado_avalancha = metodo_avalancha(deudas_info, float(pago_extra_decimal))
                resultado_bola_nieve = metodo_bola_nieve(deudas_info, float(pago_extra_decimal))
                
                resultados = {
                    'avalancha': resultado_avalancha,
                    'bola_nieve': resultado_bola_nieve,
                    'ahorro': resultado_bola_nieve['total_intereses'] - resultado_avalancha['total_intereses'],
                    'diferencia_meses': resultado_bola_nieve['meses'] - resultado_avalancha['meses']
                }
                
        except (ValueError, TypeError) as e:
            flash(f'Error en los datos ingresados: {str(e)}', 'error')
    
    return render_template('estrategias/estrategias.html', 
                         deudas=deudas, 
                         resultados=resultados)

