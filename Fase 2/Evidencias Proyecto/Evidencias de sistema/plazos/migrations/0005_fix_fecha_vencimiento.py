# Generated manually to fix fecha_vencimiento field

from django.db import migrations, models
from datetime import date, timedelta

def populate_fecha_vencimiento(apps, schema_editor):
    """Poblar fecha_vencimiento para registros existentes"""
    PlazoJudicial = apps.get_model('plazos', 'PlazoJudicial')
    
    for plazo in PlazoJudicial.objects.filter(fecha_vencimiento__isnull=True):
        if plazo.fecha_inicio and plazo.dias_plazo and plazo.tipo_dia:
            # Calcular fecha_vencimiento usando la lógica existente
            from plazos.utils.plazos import calcular_fecha_vencimiento
            plazo.fecha_vencimiento = calcular_fecha_vencimiento(
                plazo.fecha_inicio,
                plazo.dias_plazo,
                plazo.tipo_dia
            )
        elif plazo.fecha_inicio:
            # Si no tiene datos suficientes, usar fecha_inicio + 30 días
            plazo.fecha_vencimiento = plazo.fecha_inicio + timedelta(days=30)
        else:
            # Si no tiene fecha_inicio, usar fecha actual + 30 días
            plazo.fecha_vencimiento = date.today() + timedelta(days=30)
        
        plazo.save()

def reverse_populate_fecha_vencimiento(apps, schema_editor):
    """Reversar el cambio (no necesario)"""
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('plazos', '0004_auto_20251003_1653'),
    ]

    operations = [
        # Primero poblar los datos
        migrations.RunPython(
            populate_fecha_vencimiento,
            reverse_populate_fecha_vencimiento
        ),
        # Luego cambiar el campo a non-nullable
        migrations.AlterField(
            model_name='plazojudicial',
            name='fecha_vencimiento',
            field=models.DateField(verbose_name='Fecha de Vencimiento'),
        ),
    ]
