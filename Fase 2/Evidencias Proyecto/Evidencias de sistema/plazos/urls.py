from django.urls import path
from . import views, views_cpc

urlpatterns = [
    path('', views.landing, name='landing'),
    path('dashboard/', views.index, name='index'),
    path('crear/', views.crear_plazo, name='crear_plazo'),
    path('calendario/', views.calendario, name='calendario'),
    path('plazo/<int:plazo_id>/', views.detalle_plazo, name='detalle_plazo'),
    path('plazo/<int:plazo_id>/editar/', views.editar_plazo, name='editar_plazo'),
    path('plazo/<int:plazo_id>/eliminar/', views.eliminar_plazo, name='eliminar_plazo'),
    path('exportar/pdf/', views.exportar_pdf_view, name='exportar_pdf'),
    path('exportar/ics/', views.exportar_ics_view, name='exportar_ics'),
    path('api/actualizar-estados/', views.actualizar_estados, name='actualizar_estados'),
    path('api/plazos-json/', views.obtener_plazos_json, name='plazos_json'),
    path('api/codigos-procedimiento/', views.api_codigos_procedimiento, name='api_codigos_procedimiento'),
    
    # URLs para gestión de códigos CPC
    path('codigos-cpc/', views_cpc.gestionar_codigos_cpc, name='gestionar_codigos_cpc'),
    path('codigos-cpc/cargar/', views_cpc.cargar_codigos_desde_bd, name='cargar_codigos_desde_bd'),
    path('codigos-cpc/api/', views_cpc.api_codigos_disponibles, name='api_codigos_disponibles'),
    path('codigos-cpc/estadisticas/', views_cpc.estadisticas_codigos_cpc, name='estadisticas_codigos_cpc'),
]
