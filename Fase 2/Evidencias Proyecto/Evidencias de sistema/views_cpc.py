"""
Vistas para la gestión de códigos de procedimiento civil.
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from .models import CodigoProcedimiento
from .scrapers.cpc_database import CPCDatabase


@login_required
def gestionar_codigos_cpc(request):
    """
    Vista para gestionar códigos de procedimiento civil.
    """
    # Obtener filtros
    tipo_documento = request.GET.get('tipo_documento', '')
    tipo_procedimiento = request.GET.get('tipo_procedimiento', '')
    busqueda = request.GET.get('busqueda', '')
    
    # Construir consulta
    codigos = CodigoProcedimiento.objects.all()
    
    if tipo_documento:
        codigos = codigos.filter(tipo_documento=tipo_documento)
    
    if tipo_procedimiento:
        codigos = codigos.filter(tipo_procedimiento=tipo_procedimiento)
    
    if busqueda:
        codigos = codigos.filter(
            Q(nombre__icontains=busqueda) |
            Q(codigo__icontains=busqueda) |
            Q(descripcion__icontains=busqueda)
        )
    
    # Paginación
    paginator = Paginator(codigos, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Obtener opciones para filtros
    tipos_documento = CodigoProcedimiento.objects.values_list('tipo_documento', flat=True).distinct()
    tipos_procedimiento = CodigoProcedimiento.objects.values_list('tipo_procedimiento', flat=True).distinct()
    
    context = {
        'page_obj': page_obj,
        'tipos_documento': tipos_documento,
        'tipos_procedimiento': tipos_procedimiento,
        'filtros': {
            'tipo_documento': tipo_documento,
            'tipo_procedimiento': tipo_procedimiento,
            'busqueda': busqueda
        }
    }
    
    return render(request, 'plazos/gestionar_codigos_cpc.html', context)


@login_required
def cargar_codigos_desde_bd(request):
    """
    Vista para cargar códigos desde la base de datos local.
    """
    if request.method == 'POST':
        try:
            # Obtener artículos desde la base de datos local
            db = CPCDatabase()
            articulos = db.obtener_todos_los_articulos()
            
            # Cargar códigos
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
                else:
                    # Actualizar si ya existe
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
            
            messages.success(
                request, 
                f'Códigos cargados exitosamente. Creados: {codigos_creados}, Actualizados: {codigos_actualizados}'
            )
            
        except Exception as e:
            messages.error(request, f'Error al cargar códigos: {e}')
    
    return redirect('gestionar_codigos_cpc')


@login_required
def api_codigos_disponibles(request):
    """
    API para obtener códigos disponibles para el formulario.
    """
    tipo_documento = request.GET.get('tipo_documento', '')
    tipo_procedimiento = request.GET.get('tipo_procedimiento', '')
    
    codigos = CodigoProcedimiento.objects.filter(activo=True)
    
    if tipo_documento:
        codigos = codigos.filter(tipo_documento=tipo_documento)
    
    if tipo_procedimiento:
        codigos = codigos.filter(tipo_procedimiento=tipo_procedimiento)
    
    data = []
    for codigo in codigos:
        data.append({
            'id': codigo.id,
            'codigo': codigo.codigo,
            'nombre': codigo.nombre,
            'tipo_documento': codigo.tipo_documento,
            'tipo_procedimiento': codigo.tipo_procedimiento,
            'dias_plazo': codigo.dias_plazo,
            'tipo_dia': codigo.tipo_dia,
            'descripcion': codigo.descripcion,
            'observaciones': codigo.observaciones
        })
    
    return JsonResponse(data, safe=False)


@login_required
def estadisticas_codigos_cpc(request):
    """
    Vista para mostrar estadísticas de códigos del CPC.
    """
    # Estadísticas generales
    total_codigos = CodigoProcedimiento.objects.count()
    codigos_activos = CodigoProcedimiento.objects.filter(activo=True).count()
    
    # Estadísticas por tipo de documento
    por_tipo_documento = {}
    for codigo in CodigoProcedimiento.objects.all():
        tipo = codigo.tipo_documento
        por_tipo_documento[tipo] = por_tipo_documento.get(tipo, 0) + 1
    
    # Estadísticas por tipo de procedimiento
    por_tipo_procedimiento = {}
    for codigo in CodigoProcedimiento.objects.all():
        tipo = codigo.tipo_procedimiento
        por_tipo_procedimiento[tipo] = por_tipo_procedimiento.get(tipo, 0) + 1
    
    # Estadísticas por días de plazo
    por_dias_plazo = {}
    for codigo in CodigoProcedimiento.objects.all():
        dias = codigo.dias_plazo
        por_dias_plazo[dias] = por_dias_plazo.get(dias, 0) + 1
    
    context = {
        'total_codigos': total_codigos,
        'codigos_activos': codigos_activos,
        'por_tipo_documento': por_tipo_documento,
        'por_tipo_procedimiento': por_tipo_procedimiento,
        'por_dias_plazo': por_dias_plazo
    }
    
    return render(request, 'plazos/estadisticas_codigos_cpc.html', context)
