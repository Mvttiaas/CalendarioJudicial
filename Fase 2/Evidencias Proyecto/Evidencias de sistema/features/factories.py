# -*- coding: utf-8 -*-
"""
Factories para generar datos de prueba realistas
"""

import factory
from django.contrib.auth import get_user_model
from plazos.models import PlazoJudicial, CodigoProcedimiento
from usuarios.models import PerfilUsuario
from datetime import date, timedelta
import random

User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    
    username = factory.Sequence(lambda n: f"usuario{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    first_name = factory.Faker('first_name', locale='es_ES')
    last_name = factory.Faker('last_name', locale='es_ES')
    tipo_usuario = factory.Iterator(['abogado', 'juez', 'asistente'])
    rut = factory.LazyFunction(lambda: f"{random.randint(10000000, 99999999)}-{random.randint(0, 9)}")
    is_active = True

class PerfilUsuarioFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PerfilUsuario
    
    usuario = factory.SubFactory(UserFactory)
    telefono = factory.Faker('phone_number', locale='es_ES')
    fecha_nacimiento = factory.Faker('date_of_birth', minimum_age=25, maximum_age=65)

class CodigoProcedimientoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CodigoProcedimiento
    
    codigo = factory.Sequence(lambda n: f"CPC-{n:03d}")
    nombre = factory.Iterator([
        "Contestación de demanda",
        "Demanda ordinaria",
        "Requerimiento de pago",
        "Reconvención",
        "Tercería",
        "Incidente",
        "Recurso de apelación",
        "Recurso de casación"
    ])
    tipo_documento = factory.Iterator(['demanda', 'contestacion', 'requerimiento', 'recurso'])
    tipo_procedimiento = factory.Iterator(['ordinario', 'sumario', 'ejecutivo', 'especial'])
    dias_plazo = factory.Iterator([5, 10, 15, 30, 60, 90])
    tipo_dia = factory.Iterator(['habil', 'corrido'])
    articulo_cpc = factory.Sequence(lambda n: f"Art. {100 + n}")
    descripcion = factory.Faker('text', max_nb_chars=200, locale='es_ES')
    observaciones = factory.Faker('text', max_nb_chars=100, locale='es_ES')

class PlazoJudicialFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PlazoJudicial
    
    usuario = factory.SubFactory(UserFactory)
    tipo_documento = factory.Iterator(['demanda', 'contestacion', 'requerimiento', 'recurso'])
    procedimiento = factory.Iterator(['ordinario', 'sumario', 'ejecutivo', 'especial'])
    dias_plazo = factory.Iterator([5, 10, 15, 30, 60, 90])
    tipo_dia = factory.Iterator(['habil', 'corrido'])
    fecha_inicio = factory.LazyFunction(lambda: date.today() + timedelta(days=random.randint(-30, 30)))
    rol = factory.Sequence(lambda n: f"R-{n:06d}-{random.randint(2020, 2025)}")
    rut_cliente = factory.LazyFunction(lambda: f"{random.randint(10000000, 99999999)}-{random.randint(0, 9)}")
    clave_cliente = factory.Faker('word', locale='es_ES')
    estado = factory.Iterator(['pendiente', 'corriendo', 'suspendido', 'vencido'])
    observaciones = factory.Faker('text', max_nb_chars=150, locale='es_ES')
