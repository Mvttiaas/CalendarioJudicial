"""
Base de datos local de artículos del Código de Procedimiento Civil.
Contiene información extraída y estructurada del CPC.
"""
from typing import List, Dict, Optional
from datetime import datetime


class CPCDatabase:
    """
    Base de datos local con artículos del Código de Procedimiento Civil.
    """
    
    def __init__(self):
        self.articulos = self._cargar_articulos_cpc()
    
    def _cargar_articulos_cpc(self) -> List[Dict]:
        """
        Carga la base de datos local de artículos del CPC.
        
        Returns:
            Lista de artículos del CPC
        """
        return [
            # PROCEDIMIENTO ORDINARIO
            {
                'codigo': 'ART. 254 CPC',
                'nombre': 'Contestación de Demanda - Procedimiento Ordinario',
                'tipo_documento': 'contestacion',
                'tipo_procedimiento': 'ordinario',
                'dias_plazo': 15,
                'tipo_dia': 'habil',
                'articulo_cpc': 'Artículo 254',
                'descripcion': 'Plazo para contestar demanda en procedimiento ordinario',
                'observaciones': 'Se cuenta desde la notificación válida',
                'activo': True,
                'texto_legal': 'El demandado deberá contestar la demanda dentro del plazo de quince días hábiles contados desde la notificación válida.',
                'fecha_actualizacion': '2025-01-03'
            },
            {
                'codigo': 'ART. 255 CPC',
                'nombre': 'Réplica - Procedimiento Ordinario',
                'tipo_documento': 'replica',
                'tipo_procedimiento': 'ordinario',
                'dias_plazo': 6,
                'tipo_dia': 'habil',
                'articulo_cpc': 'Artículo 255',
                'descripcion': 'Plazo para replicar en procedimiento ordinario',
                'observaciones': 'Se cuenta desde la contestación',
                'activo': True,
                'texto_legal': 'El demandante podrá replicar dentro del plazo de seis días hábiles contados desde la contestación.',
                'fecha_actualizacion': '2025-01-03'
            },
            {
                'codigo': 'ART. 256 CPC',
                'nombre': 'Dúplica - Procedimiento Ordinario',
                'tipo_documento': 'duplica',
                'tipo_procedimiento': 'ordinario',
                'dias_plazo': 3,
                'tipo_dia': 'habil',
                'articulo_cpc': 'Artículo 256',
                'descripcion': 'Plazo para duplicar en procedimiento ordinario',
                'observaciones': 'Se cuenta desde la réplica',
                'activo': True,
                'texto_legal': 'El demandado podrá duplicar dentro del plazo de tres días hábiles contados desde la réplica.',
                'fecha_actualizacion': '2025-01-03'
            },
            
            # PROCEDIMIENTO SUMARIO
            {
                'codigo': 'ART. 194 CPC',
                'nombre': 'Contestación - Procedimiento Sumario',
                'tipo_documento': 'contestacion',
                'tipo_procedimiento': 'sumario',
                'dias_plazo': 10,
                'tipo_dia': 'habil',
                'articulo_cpc': 'Artículo 194',
                'descripcion': 'Plazo para contestar en procedimiento sumario',
                'observaciones': 'Se cuenta desde la notificación',
                'activo': True,
                'texto_legal': 'En el procedimiento sumario, el demandado deberá contestar dentro del plazo de diez días hábiles.',
                'fecha_actualizacion': '2025-01-03'
            },
            {
                'codigo': 'ART. 195 CPC',
                'nombre': 'Réplica - Procedimiento Sumario',
                'tipo_documento': 'replica',
                'tipo_procedimiento': 'sumario',
                'dias_plazo': 3,
                'tipo_dia': 'habil',
                'articulo_cpc': 'Artículo 195',
                'descripcion': 'Plazo para replicar en procedimiento sumario',
                'observaciones': 'Se cuenta desde la contestación',
                'activo': True,
                'texto_legal': 'En el procedimiento sumario, la réplica deberá presentarse dentro de tres días hábiles.',
                'fecha_actualizacion': '2025-01-03'
            },
            
            # PROCEDIMIENTO EJECUTIVO
            {
                'codigo': 'ART. 187 CPC',
                'nombre': 'Contestación - Procedimiento Ejecutivo',
                'tipo_documento': 'contestacion',
                'tipo_procedimiento': 'ejecutivo',
                'dias_plazo': 3,
                'tipo_dia': 'habil',
                'articulo_cpc': 'Artículo 187',
                'descripcion': 'Plazo para contestar en procedimiento ejecutivo',
                'observaciones': 'Se cuenta desde la notificación',
                'activo': True,
                'texto_legal': 'En el procedimiento ejecutivo, la contestación deberá presentarse dentro de tres días hábiles.',
                'fecha_actualizacion': '2025-01-03'
            },
            {
                'codigo': 'ART. 188 CPC',
                'nombre': 'Réplica - Procedimiento Ejecutivo',
                'tipo_documento': 'replica',
                'tipo_procedimiento': 'ejecutivo',
                'dias_plazo': 3,
                'tipo_dia': 'habil',
                'articulo_cpc': 'Artículo 188',
                'descripcion': 'Plazo para replicar en procedimiento ejecutivo',
                'observaciones': 'Se cuenta desde la contestación',
                'activo': True,
                'texto_legal': 'En el procedimiento ejecutivo, la réplica deberá presentarse dentro de tres días hábiles.',
                'fecha_actualizacion': '2025-01-03'
            },
            
            # PROCEDIMIENTO MONITORIO
            {
                'codigo': 'ART. 190 CPC',
                'nombre': 'Contestación - Procedimiento Monitorio',
                'tipo_documento': 'contestacion',
                'tipo_procedimiento': 'monitorio',
                'dias_plazo': 15,
                'tipo_dia': 'habil',
                'articulo_cpc': 'Artículo 190',
                'descripcion': 'Plazo para contestar en procedimiento monitorio',
                'observaciones': 'Se cuenta desde la notificación',
                'activo': True,
                'texto_legal': 'En el procedimiento monitorio, la contestación deberá presentarse dentro de quince días hábiles.',
                'fecha_actualizacion': '2025-01-03'
            },
            
            # RECURSOS
            {
                'codigo': 'ART. 193 CPC',
                'nombre': 'Recurso de Apelación - Procedimiento Ordinario',
                'tipo_documento': 'recurso_apelacion',
                'tipo_procedimiento': 'ordinario',
                'dias_plazo': 5,
                'tipo_dia': 'habil',
                'articulo_cpc': 'Artículo 193',
                'descripcion': 'Plazo para interponer recurso de apelación',
                'observaciones': 'Se cuenta desde la notificación de la sentencia',
                'activo': True,
                'texto_legal': 'El recurso de apelación deberá interponerse dentro del plazo de cinco días hábiles contados desde la notificación de la sentencia.',
                'fecha_actualizacion': '2025-01-03'
            },
            {
                'codigo': 'ART. 197 CPC',
                'nombre': 'Recurso de Casación',
                'tipo_documento': 'recurso_casacion',
                'tipo_procedimiento': 'ordinario',
                'dias_plazo': 10,
                'tipo_dia': 'habil',
                'articulo_cpc': 'Artículo 197',
                'descripcion': 'Plazo para interponer recurso de casación',
                'observaciones': 'Se cuenta desde la notificación de la sentencia de segunda instancia',
                'activo': True,
                'texto_legal': 'El recurso de casación deberá interponerse dentro del plazo de diez días hábiles contados desde la notificación de la sentencia de segunda instancia.',
                'fecha_actualizacion': '2025-01-03'
            },
            {
                'codigo': 'ART. 198 CPC',
                'nombre': 'Recurso de Revisión',
                'tipo_documento': 'recurso_revision',
                'tipo_procedimiento': 'ordinario',
                'dias_plazo': 30,
                'tipo_dia': 'corrido',
                'articulo_cpc': 'Artículo 198',
                'descripcion': 'Plazo para interponer recurso de revisión',
                'observaciones': 'Se cuenta desde el conocimiento del hecho que lo motiva',
                'activo': True,
                'texto_legal': 'El recurso de revisión deberá interponerse dentro del plazo de treinta días corridos contados desde el conocimiento del hecho que lo motiva.',
                'fecha_actualizacion': '2025-01-03'
            },
            {
                'codigo': 'ART. 199 CPC',
                'nombre': 'Recurso de Queja',
                'tipo_documento': 'recurso_queja',
                'tipo_procedimiento': 'ordinario',
                'dias_plazo': 5,
                'tipo_dia': 'habil',
                'articulo_cpc': 'Artículo 199',
                'descripcion': 'Plazo para interponer recurso de queja',
                'observaciones': 'Se cuenta desde la notificación del auto o resolución',
                'activo': True,
                'texto_legal': 'El recurso de queja deberá interponerse dentro del plazo de cinco días hábiles contados desde la notificación del auto o resolución.',
                'fecha_actualizacion': '2025-01-03'
            },
            
            # RECURSOS CONSTITUCIONALES
            {
                'codigo': 'ART. 200 CPC',
                'nombre': 'Recurso de Protección',
                'tipo_documento': 'recurso_proteccion',
                'tipo_procedimiento': 'constitucional',
                'dias_plazo': 30,
                'tipo_dia': 'corrido',
                'articulo_cpc': 'Artículo 200',
                'descripcion': 'Plazo para interponer recurso de protección',
                'observaciones': 'Se cuenta desde la notificación del acto que se impugna',
                'activo': True,
                'texto_legal': 'El recurso de protección deberá interponerse dentro del plazo de treinta días corridos contados desde la notificación del acto que se impugna.',
                'fecha_actualizacion': '2025-01-03'
            },
            {
                'codigo': 'ART. 201 CPC',
                'nombre': 'Recurso de Amparo',
                'tipo_documento': 'recurso_amparo',
                'tipo_procedimiento': 'constitucional',
                'dias_plazo': 30,
                'tipo_dia': 'corrido',
                'articulo_cpc': 'Artículo 201',
                'descripcion': 'Plazo para interponer recurso de amparo',
                'observaciones': 'Se cuenta desde la notificación del acto que se impugna',
                'activo': True,
                'texto_legal': 'El recurso de amparo deberá interponerse dentro del plazo de treinta días corridos contados desde la notificación del acto que se impugna.',
                'fecha_actualizacion': '2025-01-03'
            },
            
            # INCIDENTES Y EXCEPCIONES
            {
                'codigo': 'ART. 203 CPC',
                'nombre': 'Incidente',
                'tipo_documento': 'incidente',
                'tipo_procedimiento': 'ordinario',
                'dias_plazo': 5,
                'tipo_dia': 'habil',
                'articulo_cpc': 'Artículo 203',
                'descripcion': 'Plazo para resolver incidente',
                'observaciones': 'Se cuenta desde la presentación del incidente',
                'activo': True,
                'texto_legal': 'Los incidentes deberán resolverse dentro del plazo de cinco días hábiles contados desde su presentación.',
                'fecha_actualizacion': '2025-01-03'
            },
            {
                'codigo': 'ART. 204 CPC',
                'nombre': 'Excepción',
                'tipo_documento': 'excepcion',
                'tipo_procedimiento': 'ordinario',
                'dias_plazo': 5,
                'tipo_dia': 'habil',
                'articulo_cpc': 'Artículo 204',
                'descripcion': 'Plazo para resolver excepción',
                'observaciones': 'Se cuenta desde la presentación de la excepción',
                'activo': True,
                'texto_legal': 'Las excepciones deberán resolverse dentro del plazo de cinco días hábiles contados desde su presentación.',
                'fecha_actualizacion': '2025-01-03'
            },
            
            # MEDIDAS CAUTELARES
            {
                'codigo': 'ART. 214 CPC',
                'nombre': 'Medida Cautelar',
                'tipo_documento': 'medida_cautelar',
                'tipo_procedimiento': 'ordinario',
                'dias_plazo': 5,
                'tipo_dia': 'habil',
                'articulo_cpc': 'Artículo 214',
                'descripcion': 'Plazo para resolver medida cautelar',
                'observaciones': 'Se cuenta desde la presentación de la medida cautelar',
                'activo': True,
                'texto_legal': 'Las medidas cautelares deberán resolverse dentro del plazo de cinco días hábiles contados desde su presentación.',
                'fecha_actualizacion': '2025-01-03'
            },
            {
                'codigo': 'ART. 215 CPC',
                'nombre': 'Embargo',
                'tipo_documento': 'embargo',
                'tipo_procedimiento': 'ejecutivo',
                'dias_plazo': 5,
                'tipo_dia': 'habil',
                'articulo_cpc': 'Artículo 215',
                'descripcion': 'Plazo para resolver embargo',
                'observaciones': 'Se cuenta desde la presentación del embargo',
                'activo': True,
                'texto_legal': 'Los embargos deberán resolverse dentro del plazo de cinco días hábiles contados desde su presentación.',
                'fecha_actualizacion': '2025-01-03'
            },
            
            # PROCEDIMIENTOS EJECUTIVOS ESPECÍFICOS
            {
                'codigo': 'ART. 217 CPC',
                'nombre': 'Demanda de Hipoteca',
                'tipo_documento': 'demanda',
                'tipo_procedimiento': 'ejecutivo',
                'dias_plazo': 3,
                'tipo_dia': 'habil',
                'articulo_cpc': 'Artículo 217',
                'descripcion': 'Plazo para contestar demanda de hipoteca',
                'observaciones': 'Se cuenta desde la notificación',
                'activo': True,
                'texto_legal': 'Las demandas de hipoteca deberán contestarse dentro del plazo de tres días hábiles.',
                'fecha_actualizacion': '2025-01-03'
            },
            {
                'codigo': 'ART. 218 CPC',
                'nombre': 'Demanda de Prenda',
                'tipo_documento': 'demanda',
                'tipo_procedimiento': 'ejecutivo',
                'dias_plazo': 3,
                'tipo_dia': 'habil',
                'articulo_cpc': 'Artículo 218',
                'descripcion': 'Plazo para contestar demanda de prenda',
                'observaciones': 'Se cuenta desde la notificación',
                'activo': True,
                'texto_legal': 'Las demandas de prenda deberán contestarse dentro del plazo de tres días hábiles.',
                'fecha_actualizacion': '2025-01-03'
            },
            {
                'codigo': 'ART. 219 CPC',
                'nombre': 'Demanda de Anticresis',
                'tipo_documento': 'demanda',
                'tipo_procedimiento': 'ejecutivo',
                'dias_plazo': 3,
                'tipo_dia': 'habil',
                'articulo_cpc': 'Artículo 219',
                'descripcion': 'Plazo para contestar demanda de anticresis',
                'observaciones': 'Se cuenta desde la notificación',
                'activo': True,
                'texto_legal': 'Las demandas de anticresis deberán contestarse dentro del plazo de tres días hábiles.',
                'fecha_actualizacion': '2025-01-03'
            }
        ]
    
    def obtener_articulos_por_tipo(self, tipo_documento: str = None, tipo_procedimiento: str = None) -> List[Dict]:
        """
        Obtiene artículos filtrados por tipo.
        
        Args:
            tipo_documento: Tipo de documento a filtrar
            tipo_procedimiento: Tipo de procedimiento a filtrar
            
        Returns:
            Lista de artículos filtrados
        """
        articulos_filtrados = self.articulos
        
        if tipo_documento:
            articulos_filtrados = [a for a in articulos_filtrados if a['tipo_documento'] == tipo_documento]
        
        if tipo_procedimiento:
            articulos_filtrados = [a for a in articulos_filtrados if a['tipo_procedimiento'] == tipo_procedimiento]
        
        return articulos_filtrados
    
    def buscar_articulo_por_codigo(self, codigo: str) -> Optional[Dict]:
        """
        Busca un artículo por su código.
        
        Args:
            codigo: Código del artículo (ej: "ART. 254 CPC")
            
        Returns:
            Diccionario con información del artículo o None
        """
        for articulo in self.articulos:
            if articulo['codigo'] == codigo:
                return articulo
        return None
    
    def obtener_todos_los_articulos(self) -> List[Dict]:
        """
        Obtiene todos los artículos disponibles.
        
        Returns:
            Lista completa de artículos
        """
        return self.articulos
    
    def obtener_estadisticas(self) -> Dict:
        """
        Obtiene estadísticas de la base de datos.
        
        Returns:
            Diccionario con estadísticas
        """
        total = len(self.articulos)
        
        por_tipo_documento = {}
        por_tipo_procedimiento = {}
        
        for articulo in self.articulos:
            tipo_doc = articulo['tipo_documento']
            tipo_proc = articulo['tipo_procedimiento']
            
            por_tipo_documento[tipo_doc] = por_tipo_documento.get(tipo_doc, 0) + 1
            por_tipo_procedimiento[tipo_proc] = por_tipo_procedimiento.get(tipo_proc, 0) + 1
        
        return {
            'total_articulos': total,
            'por_tipo_documento': por_tipo_documento,
            'por_tipo_procedimiento': por_tipo_procedimiento
        }


def obtener_articulos_cpc_desde_bd() -> List[Dict]:
    """
    Función principal para obtener artículos del CPC desde la base de datos local.
    
    Returns:
        Lista de artículos del CPC
    """
    db = CPCDatabase()
    return db.obtener_todos_los_articulos()


if __name__ == '__main__':
    db = CPCDatabase()
    articulos = db.obtener_todos_los_articulos()
    stats = db.obtener_estadisticas()
    
    print(f"Total de artículos: {stats['total_articulos']}")
    print("\nPor tipo de documento:")
    for tipo, count in stats['por_tipo_documento'].items():
        print(f"  {tipo}: {count}")
    
    print("\nPor tipo de procedimiento:")
    for tipo, count in stats['por_tipo_procedimiento'].items():
        print(f"  {tipo}: {count}")
