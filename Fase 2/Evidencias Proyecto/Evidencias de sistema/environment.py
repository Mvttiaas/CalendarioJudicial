# -*- coding: utf-8 -*-
"""
Configuración del entorno para pruebas con Behave
"""
import os
import sys
import django
from django.conf import settings
from django.test import Client
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'calendario_judicial.settings_dev')
django.setup()

def before_all(context):
    """Configuración inicial antes de ejecutar todas las pruebas"""
    context.base_url = "http://localhost:8000"
    context.client = Client()
    print("Entorno de pruebas configurado")

def after_all(context):
    """Limpieza después de ejecutar todas las pruebas"""
    print("Pruebas completadas")

def before_scenario(context, scenario):
    """Configuración antes de cada escenario"""
    context.scenario_name = scenario.name
    print(f"Ejecutando: {scenario.name}")

def after_scenario(context, scenario):
    """Limpieza después de cada escenario"""
    if scenario.status == "failed":
        print(f"Fallo: {scenario.name}")
    else:
        print(f"Paso: {scenario.name}")
