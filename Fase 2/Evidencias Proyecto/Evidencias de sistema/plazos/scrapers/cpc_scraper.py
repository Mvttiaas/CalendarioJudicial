"""
Scraper para extraer artículos del Código de Procedimiento Civil chileno.
"""
import requests
from bs4 import BeautifulSoup
import re
from typing import List, Dict, Optional
import time
from datetime import datetime


class CPCScraper:
    """
    Scraper para extraer información del Código de Procedimiento Civil.
    """
    
    def __init__(self):
        self.base_url = "https://www.leychile.cl"
        self.search_url = "https://www.leychile.cl/Consulta/buscar"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def buscar_articulos_cpc(self, terminos_busqueda: List[str]) -> List[Dict]:
        """
        Busca artículos del CPC basado en términos de búsqueda.
        
        Args:
            terminos_busqueda: Lista de términos para buscar
            
        Returns:
            Lista de diccionarios con información de artículos
        """
        articulos_encontrados = []
        
        for termino in terminos_busqueda:
            print(f"Buscando: {termino}")
            articulos = self._buscar_termino(termino)
            articulos_encontrados.extend(articulos)
            time.sleep(1)  # Pausa para no sobrecargar el servidor
        
        # Eliminar duplicados
        articulos_unicos = self._eliminar_duplicados(articulos_encontrados)
        return articulos_unicos
    
    def _buscar_termino(self, termino: str) -> List[Dict]:
        """
        Busca un término específico en LeyChile.
        
        Args:
            termino: Término a buscar
            
        Returns:
            Lista de artículos encontrados
        """
        try:
            # Parámetros de búsqueda
            params = {
                'q': termino,
                't': '1',  # Tipo: Leyes
                'f': '0',  # Fecha desde
                'h': '0',  # Fecha hasta
                's': '0',  # Orden
                'p': '1'   # Página
            }
            
            response = self.session.get(self.search_url, params=params, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            return self._parsear_resultados(soup, termino)
            
        except Exception as e:
            print(f"Error al buscar '{termino}': {e}")
            return []
    
    def _parsear_resultados(self, soup: BeautifulSoup, termino: str) -> List[Dict]:
        """
        Parsea los resultados de búsqueda.
        
        Args:
            soup: Objeto BeautifulSoup con el HTML
            termino: Término buscado
            
        Returns:
            Lista de artículos parseados
        """
        articulos = []
        
        # Buscar enlaces a leyes
        enlaces = soup.find_all('a', href=re.compile(r'/Navegar\?idNorma='))
        
        for enlace in enlaces:
            try:
                titulo = enlace.get_text(strip=True)
                url = self.base_url + enlace.get('href')
                
                # Verificar si es del CPC
                if self._es_codigo_procedimiento_civil(titulo):
                    articulo = self._extraer_articulo_desde_url(url, termino)
                    if articulo:
                        articulos.append(articulo)
                        
            except Exception as e:
                print(f"Error al parsear enlace: {e}")
                continue
        
        return articulos
    
    def _es_codigo_procedimiento_civil(self, titulo: str) -> bool:
        """
        Verifica si el título corresponde al Código de Procedimiento Civil.
        
        Args:
            titulo: Título de la ley
            
        Returns:
            True si es del CPC
        """
        titulo_lower = titulo.lower()
        return any(palabra in titulo_lower for palabra in [
            'código de procedimiento civil',
            'codigo de procedimiento civil',
            'cpc',
            'procedimiento civil'
        ])
    
    def _extraer_articulo_desde_url(self, url: str, termino: str) -> Optional[Dict]:
        """
        Extrae información de un artículo específico desde su URL.
        
        Args:
            url: URL del artículo
            termino: Término que llevó a este artículo
            
        Returns:
            Diccionario con información del artículo o None
        """
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extraer información del artículo
            articulo_info = self._parsear_articulo(soup, termino)
            return articulo_info
            
        except Exception as e:
            print(f"Error al extraer artículo desde {url}: {e}")
            return None
    
    def _parsear_articulo(self, soup: BeautifulSoup, termino: str) -> Optional[Dict]:
        """
        Parsea la información de un artículo específico.
        
        Args:
            soup: Objeto BeautifulSoup del artículo
            termino: Término que llevó a este artículo
            
        Returns:
            Diccionario con información del artículo
        """
        try:
            # Buscar el número del artículo
            numero_articulo = self._extraer_numero_articulo(soup)
            if not numero_articulo:
                return None
            
            # Extraer texto del artículo
            texto_articulo = self._extraer_texto_articulo(soup)
            
            # Determinar tipo de documento y procedimiento
            tipo_info = self._determinar_tipo_documento(termino, texto_articulo)
            
            # Extraer días de plazo
            dias_plazo = self._extraer_dias_plazo(texto_articulo)
            
            # Determinar tipo de día
            tipo_dia = self._determinar_tipo_dia(texto_articulo)
            
            return {
                'codigo': f"ART. {numero_articulo} CPC",
                'nombre': f"{tipo_info['tipo_documento']} - {tipo_info['tipo_procedimiento']}",
                'tipo_documento': tipo_info['tipo_documento'],
                'tipo_procedimiento': tipo_info['tipo_procedimiento'],
                'dias_plazo': dias_plazo,
                'tipo_dia': tipo_dia,
                'articulo_cpc': f"Artículo {numero_articulo}",
                'descripcion': f"Plazo para {tipo_info['tipo_documento']} en {tipo_info['tipo_procedimiento']}",
                'observaciones': f"Se cuenta desde {self._extraer_observaciones(texto_articulo)}",
                'activo': True,
                'texto_completo': texto_articulo,
                'fecha_extraccion': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error al parsear artículo: {e}")
            return None
    
    def _extraer_numero_articulo(self, soup: BeautifulSoup) -> Optional[str]:
        """Extrae el número del artículo."""
        # Buscar patrones como "Artículo 254", "Art. 255", etc.
        patrones = [
            r'Artículo\s+(\d+)',
            r'Art\.\s*(\d+)',
            r'Art\s+(\d+)'
        ]
        
        texto = soup.get_text()
        for patron in patrones:
            match = re.search(patron, texto, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None
    
    def _extraer_texto_articulo(self, soup: BeautifulSoup) -> str:
        """Extrae el texto completo del artículo."""
        # Buscar el contenido principal
        contenido = soup.find('div', class_='contenido') or soup.find('div', class_='texto')
        if contenido:
            return contenido.get_text(strip=True)
        
        return soup.get_text(strip=True)
    
    def _determinar_tipo_documento(self, termino: str, texto: str) -> Dict[str, str]:
        """Determina el tipo de documento y procedimiento."""
        termino_lower = termino.lower()
        texto_lower = texto.lower()
        
        # Mapeo de términos a tipos de documento
        tipos_documento = {
            'contestacion': ['contestación', 'contestar', 'contestar'],
            'replica': ['réplica', 'replicar', 'replica'],
            'duplica': ['dúplica', 'duplicar', 'duplica'],
            'recurso_apelacion': ['recurso de apelación', 'apelación', 'apelar'],
            'recurso_casacion': ['recurso de casación', 'casación', 'casar'],
            'recurso_revision': ['recurso de revisión', 'revisión', 'revisar'],
            'recurso_queja': ['recurso de queja', 'queja', 'quejar'],
            'recurso_proteccion': ['recurso de protección', 'protección', 'proteger'],
            'recurso_amparo': ['recurso de amparo', 'amparo', 'amparar'],
            'incidente': ['incidente', 'incidentes'],
            'excepcion': ['excepción', 'excepciones', 'exceptuar'],
            'medida_cautelar': ['medida cautelar', 'cautelar', 'cautelas'],
            'embargo': ['embargo', 'embargar', 'embargos']
        }
        
        # Determinar tipo de documento
        tipo_documento = 'otro'
        for tipo, palabras in tipos_documento.items():
            if any(palabra in termino_lower or palabra in texto_lower for palabra in palabras):
                tipo_documento = tipo
                break
        
        # Determinar tipo de procedimiento
        tipo_procedimiento = 'ordinario'
        if 'sumario' in texto_lower:
            tipo_procedimiento = 'sumario'
        elif 'ejecutivo' in texto_lower:
            tipo_procedimiento = 'ejecutivo'
        elif 'monitorio' in texto_lower:
            tipo_procedimiento = 'monitorio'
        elif 'constitucional' in texto_lower or 'protección' in texto_lower or 'amparo' in texto_lower:
            tipo_procedimiento = 'constitucional'
        
        return {
            'tipo_documento': tipo_documento,
            'tipo_procedimiento': tipo_procedimiento
        }
    
    def _extraer_dias_plazo(self, texto: str) -> int:
        """Extrae el número de días de plazo del texto."""
        # Patrones para buscar días
        patrones = [
            r'(\d+)\s*días?\s*hábiles?',
            r'(\d+)\s*días?\s*corridos?',
            r'(\d+)\s*días?',
            r'plazo\s*de\s*(\d+)\s*días?'
        ]
        
        for patron in patrones:
            match = re.search(patron, texto, re.IGNORECASE)
            if match:
                return int(match.group(1))
        
        # Valores por defecto según el tipo de documento
        if 'contestación' in texto.lower():
            return 15
        elif 'réplica' in texto.lower():
            return 6
        elif 'dúplica' in texto.lower():
            return 3
        elif 'recurso' in texto.lower():
            return 5
        
        return 30  # Valor por defecto
    
    def _determinar_tipo_dia(self, texto: str) -> str:
        """Determina si son días hábiles o corridos."""
        texto_lower = texto.lower()
        
        if 'hábil' in texto_lower or 'hábiles' in texto_lower:
            return 'habil'
        elif 'corrido' in texto_lower or 'corridos' in texto_lower:
            return 'corrido'
        elif 'recurso de protección' in texto_lower or 'recurso de amparo' in texto_lower:
            return 'corrido'
        else:
            return 'habil'  # Por defecto son hábiles
    
    def _extraer_observaciones(self, texto: str) -> str:
        """Extrae observaciones sobre el cómputo del plazo."""
        texto_lower = texto.lower()
        
        if 'notificación' in texto_lower:
            return 'la notificación'
        elif 'presentación' in texto_lower:
            return 'la presentación'
        elif 'conocimiento' in texto_lower:
            return 'el conocimiento del hecho'
        else:
            return 'la fecha correspondiente'
    
    def _eliminar_duplicados(self, articulos: List[Dict]) -> List[Dict]:
        """Elimina artículos duplicados basado en el código."""
        vistos = set()
        unicos = []
        
        for articulo in articulos:
            codigo = articulo.get('codigo')
            if codigo and codigo not in vistos:
                vistos.add(codigo)
                unicos.append(articulo)
        
        return unicos


def obtener_articulos_cpc_automaticamente() -> List[Dict]:
    """
    Función principal para obtener artículos del CPC automáticamente.
    
    Returns:
        Lista de artículos extraídos
    """
    scraper = CPCScraper()
    
    # Términos de búsqueda para encontrar artículos relevantes
    terminos_busqueda = [
        'contestación demanda procedimiento',
        'réplica procedimiento civil',
        'dúplica procedimiento',
        'recurso apelación procedimiento',
        'recurso casación',
        'recurso revisión',
        'recurso queja',
        'recurso protección',
        'recurso amparo',
        'incidente procedimiento civil',
        'excepción procedimiento',
        'medida cautelar',
        'embargo procedimiento'
    ]
    
    print("Iniciando extracción automática de artículos del CPC...")
    articulos = scraper.buscar_articulos_cpc(terminos_busqueda)
    
    print(f"Se encontraron {len(articulos)} artículos del CPC")
    return articulos


if __name__ == '__main__':
    articulos = obtener_articulos_cpc_automaticamente()
    for articulo in articulos:
        print(f"- {articulo['codigo']}: {articulo['nombre']}")
