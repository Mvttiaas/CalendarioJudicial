# -*- coding: utf-8 -*-
"""
Pasos específicos para pruebas de plazos judiciales
"""
from behave import given, when, then
from datetime import date, timedelta
from plazos.utils import calcular_fecha_vencimiento


@when('cambio el estado del plazo a {estado}')
def step_cambio_estado_plazo(context, estado):
    """Cambiar el estado de un plazo"""
    context.plazo.estado = estado
    context.plazo.save()

@then('el plazo debería estar {condicion}')
def step_plazo_deberia_estar(context, condicion):
    """Verificar condición específica del plazo"""
    context.plazo.refresh_from_db()
    
    if condicion == "vencido":
        assert context.plazo.dias_restantes < 0
    elif condicion == "vigente":
        assert context.plazo.dias_restantes >= 0
    elif condicion == "suspendido":
        assert context.plazo.estado == "suspendido"

