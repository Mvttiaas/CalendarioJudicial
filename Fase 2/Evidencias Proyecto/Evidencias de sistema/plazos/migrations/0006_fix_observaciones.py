# Generated manually to fix observaciones field

from django.db import migrations, models

def populate_observaciones(apps, schema_editor):
    """Poblar observaciones para registros existentes"""
    PlazoJudicial = apps.get_model('plazos', 'PlazoJudicial')
    
    for plazo in PlazoJudicial.objects.filter(observaciones__isnull=True):
        plazo.observaciones = ""
        plazo.save()

def reverse_populate_observaciones(apps, schema_editor):
    """Reversar el cambio (no necesario)"""
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('plazos', '0005_fix_fecha_vencimiento'),
    ]

    operations = [
        # Primero poblar los datos
        migrations.RunPython(
            populate_observaciones,
            reverse_populate_observaciones
        ),
        # Luego cambiar el campo a non-nullable
        migrations.AlterField(
            model_name='plazojudicial',
            name='observaciones',
            field=models.TextField(blank=True, verbose_name='Observaciones'),
        ),
    ]
