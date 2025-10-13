from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from datetime import date, timedelta
from .models import PlazoJudicial, CodigoProcedimiento
from .forms import PlazoJudicialForm, FiltroPlazosForm
from .utils.plazos import es_plazo_urgente, formatear_fecha_chilena
# from .utils.export import exportar_pdf, exportar_ics
import json


def landing(request):
    """
    Página de introducción para usuarios no autenticados.
    """
    if request.user.is_authenticated:
        return redirect('index')
    
    return render(request, 'plazos/landing.html')

def index(request):
    """
    Vista principal que muestra el dashboard con estadísticas y plazos recientes.
    Solo muestra plazos del usuario actual.
    """
    if not request.user.is_authenticated:
        return redirect('landing')
    
    # Filtrar solo plazos del usuario actual
    plazos_usuario = PlazoJudicial.objects.filter(usuario=request.user)
    
    # Estadísticas del usuario
    total_plazos = plazos_usuario.count()
    plazos_vencidos = plazos_usuario.filter(estado='vencido').count()
    plazos_corriendo = plazos_usuario.filter(estado='corriendo').count()
    plazos_urgentes = plazos_usuario.filter(
        fecha_vencimiento__lte=date.today() + timedelta(days=3),
        estado__in=['corriendo', 'pendiente']
    ).count()
    
    # Plazos recientes del usuario (últimos 10)
    plazos_recientes = plazos_usuario.order_by('-created_at')[:10]
    
    # Plazos que vencen en los próximos 7 días del usuario
    plazos_proximos = plazos_usuario.filter(
        fecha_vencimiento__lte=date.today() + timedelta(days=7),
        fecha_vencimiento__gte=date.today(),
        estado__in=['corriendo', 'pendiente']
    ).order_by('fecha_vencimiento')[:5]
    
    # Verificar si es un usuario nuevo (sin plazos)
    es_usuario_nuevo = total_plazos == 0
    
    context = {
        'total_plazos': total_plazos,
        'plazos_vencidos': plazos_vencidos,
        'plazos_corriendo': plazos_corriendo,
        'plazos_urgentes': plazos_urgentes,
        'plazos_recientes': plazos_recientes,
        'plazos_proximos': plazos_proximos,
        'es_usuario_nuevo': es_usuario_nuevo,
    }
    
    return render(request, 'plazos/index.html', context)


@login_required
def crear_plazo(request):
    """
    Vista para crear un nuevo plazo judicial.
    """
    if request.method == 'POST':
        form = PlazoJudicialForm(request.POST, request.FILES)
        if form.is_valid():
            plazo = form.save(commit=False)
            plazo.usuario = request.user
            plazo.save()
            if plazo.fecha_vencimiento:
                fecha_venc = formatear_fecha_chilena(plazo.fecha_vencimiento)
            else:
                fecha_venc = "No calculada"
            
            messages.success(
                request, 
                f'Plazo judicial creado exitosamente. '
                f'Fecha de vencimiento: {fecha_venc}'
            )
            return redirect('calendario')
    else:
        form = PlazoJudicialForm()
    
    return render(request, 'plazos/crear_plazo.html', {'form': form})


@login_required
def calendario(request):
    """
    Vista principal del calendario que muestra los plazos del usuario con filtros avanzados.
    """
    # Obtener parámetros de filtro
    form_filtro = FiltroPlazosForm(request.GET)
    
    # Query base - solo plazos del usuario actual
    plazos = PlazoJudicial.objects.filter(usuario=request.user)
    
    # Aplicar filtros
    if form_filtro.is_valid():
        # Filtros básicos
        if form_filtro.cleaned_data.get('tipo_documento'):
            plazos = plazos.filter(tipo_documento=form_filtro.cleaned_data['tipo_documento'])
        
        if form_filtro.cleaned_data.get('procedimiento'):
            plazos = plazos.filter(procedimiento=form_filtro.cleaned_data['procedimiento'])
        
        if form_filtro.cleaned_data.get('estado'):
            plazos = plazos.filter(estado=form_filtro.cleaned_data['estado'])
        
        # Filtros de fecha
        if form_filtro.cleaned_data.get('fecha_desde'):
            plazos = plazos.filter(fecha_vencimiento__gte=form_filtro.cleaned_data['fecha_desde'])
        
        if form_filtro.cleaned_data.get('fecha_hasta'):
            plazos = plazos.filter(fecha_vencimiento__lte=form_filtro.cleaned_data['fecha_hasta'])
        
        # Búsqueda general avanzada
        if form_filtro.cleaned_data.get('busqueda'):
            busqueda = form_filtro.cleaned_data['busqueda']
            busqueda_exacta = form_filtro.cleaned_data.get('busqueda_exacta', False)
            incluir_observaciones = form_filtro.cleaned_data.get('incluir_observaciones', True)
            
            # Construir query de búsqueda
            search_queries = Q()
            
            if busqueda_exacta:
                # Búsqueda exacta
                search_queries |= Q(rol__iexact=busqueda)
                search_queries |= Q(clave_cliente__iexact=busqueda)
                if incluir_observaciones:
                    search_queries |= Q(observaciones__iexact=busqueda)
            else:
                # Búsqueda parcial (icontains)
                search_queries |= Q(rol__icontains=busqueda)
                search_queries |= Q(clave_cliente__icontains=busqueda)
                if incluir_observaciones:
                    search_queries |= Q(observaciones__icontains=busqueda)
            
            plazos = plazos.filter(search_queries)
        
        # Búsqueda específica
        if form_filtro.cleaned_data.get('rol'):
            plazos = plazos.filter(rol__icontains=form_filtro.cleaned_data['rol'])
        
        if form_filtro.cleaned_data.get('rut_cliente'):
            plazos = plazos.filter(rut_cliente__icontains=form_filtro.cleaned_data['rut_cliente'])
        
        if form_filtro.cleaned_data.get('clave_cliente'):
            plazos = plazos.filter(clave_cliente__icontains=form_filtro.cleaned_data['clave_cliente'])
        
        # Filtros especiales
        if form_filtro.cleaned_data.get('solo_urgentes'):
            plazos = plazos.filter(
                fecha_vencimiento__lte=date.today() + timedelta(days=3),
                estado__in=['corriendo', 'pendiente']
            )
        
        if form_filtro.cleaned_data.get('solo_vencidos'):
            plazos = plazos.filter(estado='vencido')
        
        # Ordenamiento
        ordenar_por = form_filtro.cleaned_data.get('ordenar_por', 'fecha_vencimiento')
        direccion = form_filtro.cleaned_data.get('direccion_orden', 'asc')
        
        # Validar que el campo de ordenamiento no esté vacío
        if not ordenar_por or ordenar_por == '':
            ordenar_por = 'fecha_vencimiento'
        
        if direccion == 'desc':
            ordenar_por = f'-{ordenar_por}'
        
        plazos = plazos.order_by(ordenar_por, 'fecha_inicio')
    else:
        # Ordenamiento por defecto
        plazos = plazos.order_by('fecha_vencimiento', 'fecha_inicio')
    
    # Paginación
    paginator = Paginator(plazos, 20)  # 20 plazos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'form_filtro': form_filtro,
        'total_plazos': plazos.count(),
    }
    
    return render(request, 'plazos/calendario.html', context)


@login_required
def editar_plazo(request, plazo_id):
    """
    Vista para editar un plazo judicial existente.
    """
    plazo = get_object_or_404(PlazoJudicial, id=plazo_id, usuario=request.user)
    
    if request.method == 'POST':
        form = PlazoJudicialForm(request.POST, request.FILES, instance=plazo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Plazo judicial actualizado exitosamente.')
            return redirect('calendario')
    else:
        form = PlazoJudicialForm(instance=plazo)
    
    context = {
        'form': form,
        'plazo': plazo,
    }
    
    return render(request, 'plazos/editar_plazo.html', context)


@login_required
def eliminar_plazo(request, plazo_id):
    """
    Vista para eliminar un plazo judicial.
    """
    plazo = get_object_or_404(PlazoJudicial, id=plazo_id, usuario=request.user)
    
    if request.method == 'POST':
        plazo.delete()
        messages.success(request, 'Plazo judicial eliminado exitosamente.')
        return redirect('calendario')
    
    context = {
        'plazo': plazo,
    }
    
    return render(request, 'plazos/eliminar_plazo.html', context)


@login_required
def detalle_plazo(request, plazo_id):
    """
    Vista para mostrar el detalle de un plazo judicial.
    """
    plazo = get_object_or_404(PlazoJudicial, id=plazo_id, usuario=request.user)
    
    # Calcular información adicional
    dias_restantes = plazo.dias_restantes
    es_urgente = es_plazo_urgente(plazo.fecha_vencimiento) if plazo.fecha_vencimiento else False
    
    context = {
        'plazo': plazo,
        'dias_restantes': dias_restantes,
        'es_urgente': es_urgente,
    }
    
    return render(request, 'plazos/detalle_plazo.html', context)


@login_required
def exportar_pdf_view(request):
    """
    Vista para exportar plazos a PDF.
    """
    from django.http import HttpResponse
    from django.template.loader import render_to_string
    from datetime import datetime
    import io
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    
    # Obtener plazos seleccionados o aplicar filtros
    plazos_seleccionados = request.GET.getlist('plazos')
    
    if plazos_seleccionados:
        # Exportar solo los plazos seleccionados
        plazos = PlazoJudicial.objects.filter(id__in=plazos_seleccionados)
        titulo = f"Plazos Seleccionados ({len(plazos)} plazos)"
    else:
        # Obtener plazos con los mismos filtros que el calendario
        form_filtro = FiltroPlazosForm(request.GET)
        plazos = PlazoJudicial.objects.filter(usuario=request.user)
        
        if form_filtro.is_valid():
            if form_filtro.cleaned_data.get('tipo_documento'):
                plazos = plazos.filter(tipo_documento=form_filtro.cleaned_data['tipo_documento'])
            if form_filtro.cleaned_data.get('procedimiento'):
                plazos = plazos.filter(procedimiento=form_filtro.cleaned_data['procedimiento'])
            if form_filtro.cleaned_data.get('estado'):
                plazos = plazos.filter(estado=form_filtro.cleaned_data['estado'])
            if form_filtro.cleaned_data.get('fecha_desde'):
                plazos = plazos.filter(fecha_vencimiento__gte=form_filtro.cleaned_data['fecha_desde'])
            if form_filtro.cleaned_data.get('fecha_hasta'):
                plazos = plazos.filter(fecha_vencimiento__lte=form_filtro.cleaned_data['fecha_hasta'])
        
        titulo = "Calendario de Plazos Judiciales"
    
    plazos = plazos.order_by('fecha_vencimiento', 'fecha_inicio')
    
    # Crear buffer para el PDF
    buffer = io.BytesIO()
    
    # Crear documento PDF con márgenes optimizados
    # Usar orientación horizontal si hay muchos plazos para mejor visualización
    if plazos.count() > 10:
        from reportlab.lib.pagesizes import landscape
        doc = SimpleDocTemplate(buffer, pagesize=landscape(A4), rightMargin=50, leftMargin=50, topMargin=72, bottomMargin=50)
    else:
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=50, leftMargin=50, topMargin=72, bottomMargin=50)
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=1  # Centrado
    )
    
    # Contenido del PDF
    story = []
    
    # Título
    story.append(Paragraph(titulo, title_style))
    story.append(Spacer(1, 12))
    
    # Información de generación
    fecha_gen = datetime.now().strftime("%d/%m/%Y %H:%M")
    story.append(Paragraph(f"Generado el: {fecha_gen}", styles['Normal']))
    story.append(Paragraph(f"Total de plazos: {plazos.count()}", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Tabla de plazos
    if plazos.exists():
        # Encabezados de la tabla con texto más corto
        data = [['Doc.', 'Procedimiento', 'Inicio', 'Vencimiento', 'Estado', 'RUT']]
        
        # Datos de los plazos
        for plazo in plazos:
            fecha_inicio = plazo.fecha_inicio.strftime("%d/%m/%Y") if plazo.fecha_inicio else "-"
            fecha_vencimiento = plazo.fecha_vencimiento.strftime("%d/%m/%Y") if plazo.fecha_vencimiento else "-"
            
            data.append([
                plazo.get_tipo_documento_display(),
                plazo.get_procedimiento_display(),
                fecha_inicio,
                fecha_vencimiento,
                plazo.get_estado_display(),
                plazo.rut_cliente
            ])
    
        # Crear tabla con anchos optimizados según orientación
        if plazos.count() > 10:
            # Orientación horizontal: más espacio disponible
            table = Table(data, colWidths=[1.5*inch, 2.5*inch, 1.2*inch, 1.2*inch, 1*inch, 1.5*inch])
        else:
            # Orientación vertical: espacio limitado
            table = Table(data, colWidths=[1.2*inch, 2*inch, 1*inch, 1*inch, 0.8*inch, 1.2*inch])
        # Aplicar estilos a la tabla
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('WRAP', (0, 0), (-1, -1), 'CENTER'),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ])
        
        # Alternar colores de filas para mejor legibilidad
        for i in range(1, len(data)):
            if i % 2 == 0:
                table_style.add('BACKGROUND', (0, i), (-1, i), colors.lightgrey)
        
        table.setStyle(table_style)
    
        story.append(table)
    else:
        story.append(Paragraph("No hay plazos para mostrar con los filtros aplicados.", styles['Normal']))
    
    # Construir PDF
    doc.build(story)
    
    # Obtener el contenido del buffer
    pdf_content = buffer.getvalue()
    buffer.close()
    
    # Crear respuesta HTTP
    response = HttpResponse(pdf_content, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="plazos_judiciales_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf"'
    
    return response


@login_required
def exportar_ics_view(request):
    """
    Vista para exportar plazos a formato iCalendar.
    """
    from django.http import HttpResponse
    from datetime import datetime
    
    # Obtener plazos seleccionados o aplicar filtros
    plazos_seleccionados = request.GET.getlist('plazos')
    
    if plazos_seleccionados:
        # Exportar solo los plazos seleccionados
        plazos = PlazoJudicial.objects.filter(id__in=plazos_seleccionados)
    else:
        # Obtener plazos con los mismos filtros que el calendario
        form_filtro = FiltroPlazosForm(request.GET)
        plazos = PlazoJudicial.objects.filter(usuario=request.user)
        
        if form_filtro.is_valid():
            if form_filtro.cleaned_data.get('tipo_documento'):
                plazos = plazos.filter(tipo_documento=form_filtro.cleaned_data['tipo_documento'])
            if form_filtro.cleaned_data.get('procedimiento'):
                plazos = plazos.filter(procedimiento=form_filtro.cleaned_data['procedimiento'])
            if form_filtro.cleaned_data.get('estado'):
                plazos = plazos.filter(estado=form_filtro.cleaned_data['estado'])
            if form_filtro.cleaned_data.get('fecha_desde'):
                plazos = plazos.filter(fecha_vencimiento__gte=form_filtro.cleaned_data['fecha_desde'])
            if form_filtro.cleaned_data.get('fecha_hasta'):
                plazos = plazos.filter(fecha_vencimiento__lte=form_filtro.cleaned_data['fecha_hasta'])
    
    plazos = plazos.order_by('fecha_vencimiento', 'fecha_inicio')
    
    # Generar iCalendar simple
    ics_content = "BEGIN:VCALENDAR\n"
    ics_content += "VERSION:2.0\n"
    ics_content += "PRODID:-//Calendario Judicial//ES\n"
    ics_content += "CALSCALE:GREGORIAN\n"
    
    for plazo in plazos:
        if plazo.fecha_vencimiento:
            ics_content += "BEGIN:VEVENT\n"
            ics_content += f"UID:plazo-{plazo.id}@calendario-judicial.local\n"
            ics_content += f"SUMMARY:{plazo.get_tipo_documento_display()} - {plazo.rol}\n"
            ics_content += f"DTSTART:{plazo.fecha_vencimiento.strftime('%Y%m%d')}\n"
            ics_content += f"DTEND:{plazo.fecha_vencimiento.strftime('%Y%m%d')}\n"
            ics_content += f"DESCRIPTION:Procedimiento: {plazo.get_procedimiento_display()}\\n"
            ics_content += f"Estado: {plazo.get_estado_display()}\\n"
            ics_content += f"Clave: {plazo.clave_cliente}\n"
            ics_content += "END:VEVENT\n"
    
    ics_content += "END:VCALENDAR\n"
    
    response = HttpResponse(ics_content, content_type='text/calendar; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="plazos_judiciales_{datetime.now().strftime("%Y%m%d_%H%M%S")}.ics"'
    
    return response


@login_required
def actualizar_estados(request):
    """
    Vista AJAX para actualizar estados de plazos.
    """
    if request.method == 'POST':
        plazos = PlazoJudicial.objects.filter(
            estado__in=['pendiente', 'corriendo']
        )
        
        actualizados = 0
        for plazo in plazos:
            estado_anterior = plazo.estado
            plazo.actualizar_estado()
            if plazo.estado != estado_anterior:
                actualizados += 1
        
        return JsonResponse({
            'success': True,
            'actualizados': actualizados,
            'message': f'Se actualizaron {actualizados} plazos.'
        })
    
    return JsonResponse({'success': False, 'message': 'Método no permitido.'})


@login_required
def obtener_plazos_json(request):
    """
    Vista AJAX para obtener plazos en formato JSON (para calendarios dinámicos).
    """
    plazos = PlazoJudicial.objects.filter(usuario=request.user)
    
    eventos = []
    for plazo in plazos:
        eventos.append({
            'id': plazo.id,
            'title': f"{plazo.get_tipo_documento_display()} - {plazo.rol}",
            'start': plazo.fecha_vencimiento.isoformat() if plazo.fecha_vencimiento else None,
            'end': plazo.fecha_vencimiento.isoformat() if plazo.fecha_vencimiento else None,
            'color': _obtener_color_estado(plazo.estado),
            'url': f'/plazos/{plazo.id}/',
        })
    
    return JsonResponse(eventos, safe=False)


def _obtener_color_estado(estado):
    """
    Obtiene el color CSS para un estado de plazo.
    """
    colores = {
        'pendiente': '#6c757d',
        'esperando_proveido': '#ffc107',
        'corriendo': '#0d6efd',
        'suspendido': '#fd7e14',
        'vencido': '#dc3545',
    }
    return colores.get(estado, '#6c757d')


@login_required
def api_codigos_procedimiento(request):
    """
    API endpoint para obtener códigos de procedimiento en formato JSON.
    """
    codigos = CodigoProcedimiento.objects.filter(activo=True).order_by('codigo')
    
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
            'articulo_cpc': codigo.articulo_cpc,
            'descripcion': codigo.descripcion,
            'observaciones': codigo.observaciones,
        })
    
    return JsonResponse(data, safe=False)
