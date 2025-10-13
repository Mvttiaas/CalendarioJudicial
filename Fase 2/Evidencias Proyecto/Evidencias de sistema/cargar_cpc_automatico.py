"""
Comando de Django para cargar automáticamente códigos del CPC.
"""
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from plazos.models import CodigoProcedimiento
from plazos.scrapers.cpc_database import obtener_articulos_cpc_desde_bd


class Command(BaseCommand):
    help = 'Carga automáticamente códigos de procedimiento civil desde la base de datos local'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limpiar',
            action='store_true',
            help='Limpiar códigos existentes antes de cargar',
        )
        parser.add_argument(
            '--tipo-documento',
            type=str,
            help='Cargar solo códigos de un tipo de documento específico',
        )
        parser.add_argument(
            '--tipo-procedimiento',
            type=str,
            help='Cargar solo códigos de un tipo de procedimiento específico',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Mostrar qué se cargaría sin ejecutar la carga',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Iniciando carga automática de códigos del CPC...')
        )

        try:
            # Obtener artículos desde la base de datos local
            articulos = obtener_articulos_cpc_desde_bd()
            
            # Filtrar si se especificó tipo
            if options['tipo_documento']:
                articulos = [a for a in articulos if a['tipo_documento'] == options['tipo_documento']]
                self.stdout.write(f"Filtrando por tipo de documento: {options['tipo_documento']}")
            
            if options['tipo_procedimiento']:
                articulos = [a for a in articulos if a['tipo_procedimiento'] == options['tipo_procedimiento']]
                self.stdout.write(f"Filtrando por tipo de procedimiento: {options['tipo_procedimiento']}")

            if options['dry_run']:
                self.stdout.write(self.style.WARNING('MODO DRY-RUN: No se realizarán cambios'))
                self._mostrar_articulos(articulos)
                return

            # Limpiar códigos existentes si se solicita
            if options['limpiar']:
                self.stdout.write('Limpiando códigos existentes...')
                CodigoProcedimiento.objects.all().delete()
                self.stdout.write(self.style.SUCCESS('Códigos existentes eliminados'))

            # Cargar códigos en una transacción
            with transaction.atomic():
                codigos_creados = 0
                codigos_actualizados = 0

                for articulo in articulos:
                    codigo, created = CodigoProcedimiento.objects.get_or_create(
                        codigo=articulo['codigo'],
                        defaults={
                            'nombre': articulo['nombre'],
                            'tipo_documento': articulo['tipo_documento'],
                            'tipo_procedimiento': articulo['tipo_procedimiento'],
                            'dias_plazo': articulo['dias_plazo'],
                            'tipo_dia': articulo['tipo_dia'],
                            'articulo_cpc': articulo['articulo_cpc'],
                            'descripcion': articulo['descripcion'],
                            'observaciones': articulo['observaciones'],
                            'activo': articulo['activo']
                        }
                    )
                    
                    if created:
                        codigos_creados += 1
                        self.stdout.write(f"  + Creado: {codigo.codigo} - {codigo.nombre}")
                    else:
                        # Actualizar campos si el código ya existe
                        codigo.nombre = articulo['nombre']
                        codigo.tipo_documento = articulo['tipo_documento']
                        codigo.tipo_procedimiento = articulo['tipo_procedimiento']
                        codigo.dias_plazo = articulo['dias_plazo']
                        codigo.tipo_dia = articulo['tipo_dia']
                        codigo.articulo_cpc = articulo['articulo_cpc']
                        codigo.descripcion = articulo['descripcion']
                        codigo.observaciones = articulo['observaciones']
                        codigo.activo = articulo['activo']
                        codigo.save()
                        codigos_actualizados += 1
                        self.stdout.write(f"  ~ Actualizado: {codigo.codigo} - {codigo.nombre}")

            # Mostrar resumen
            self._mostrar_resumen(codigos_creados, codigos_actualizados, articulos)

        except Exception as e:
            raise CommandError(f'Error al cargar códigos: {e}')

    def _mostrar_articulos(self, articulos):
        """Muestra los artículos que se cargarían."""
        self.stdout.write(f'\nSe cargarían {len(articulos)} artículos:')
        for articulo in articulos:
            self.stdout.write(f"  - {articulo['codigo']}: {articulo['nombre']}")

    def _mostrar_resumen(self, creados, actualizados, articulos):
        """Muestra el resumen de la operación."""
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('CARGA COMPLETADA EXITOSAMENTE'))
        self.stdout.write('='*60)
        self.stdout.write(f'Códigos creados: {creados}')
        self.stdout.write(f'Códigos actualizados: {actualizados}')
        self.stdout.write(f'Total procesados: {len(articulos)}')
        
        # Mostrar estadísticas por tipo
        tipos_doc = {}
        tipos_proc = {}
        
        for articulo in articulos:
            tipo_doc = articulo['tipo_documento']
            tipo_proc = articulo['tipo_procedimiento']
            
            tipos_doc[tipo_doc] = tipos_doc.get(tipo_doc, 0) + 1
            tipos_proc[tipo_proc] = tipos_proc.get(tipo_proc, 0) + 1
        
        self.stdout.write('\nPor tipo de documento:')
        for tipo, count in tipos_doc.items():
            self.stdout.write(f'  {tipo}: {count} códigos')
        
        self.stdout.write('\nPor tipo de procedimiento:')
        for tipo, count in tipos_proc.items():
            self.stdout.write(f'  {tipo}: {count} códigos')
