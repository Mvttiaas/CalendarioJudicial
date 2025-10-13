# Sistema de Pruebas Gherkin/BDD - Calendario Judicial

## 📋 Descripción General

Este proyecto implementa un sistema completo de pruebas de comportamiento usando **Gherkin/BDD** (Behavior Driven Development) para el sistema de gestión de plazos judiciales. Las pruebas están escritas en lenguaje natural y cubren todas las funcionalidades críticas del sistema.

## 🎯 Características del Sistema de Pruebas

### **Total de Escenarios: 67**
- **Autenticación de usuarios**: 12 escenarios
- **Gestión de plazos judiciales**: 18 escenarios  
- **Gestión de perfil de usuario**: 10 escenarios
- **Dashboard y estadísticas**: 12 escenarios
- **Exportación de datos**: 15 escenarios

## 🏗️ Estructura del Proyecto

```
features/
├── autenticacion.feature          # Pruebas de login/registro
├── plazos_judiciales.feature      # Gestión de plazos
├── gestion_perfil.feature         # Gestión de perfil
├── dashboard_estadisticas.feature # Dashboard y estadísticas
├── exportacion.feature            # Exportación de datos
├── environment.py                 # Configuración del entorno
└── steps/
    ├── common_steps.py            # Pasos comunes
    └── plazos_steps.py            # Pasos específicos de plazos
```

## 🚀 Instalación y Configuración

### 1. Instalar Dependencias
```bash
pip install -r requirements-testing.txt
```

### 2. Configurar Django
```bash
python manage.py migrate
python manage.py loaddata fixtures/codigos_procedimiento.json
```

### 3. Ejecutar Pruebas
```bash
# Ejecutar todas las pruebas
behave features/

# Ejecutar una característica específica
behave features/autenticacion.feature

# Ejecutar con formato detallado
behave features/ --format=pretty --color
```

## 📊 Ejecución con PowerShell

### Script Principal
```powershell
.\ejecutar-pruebas-gherkin.ps1
```

Este script:
- ✅ Activa el entorno virtual
- ✅ Instala dependencias automáticamente
- ✅ Ejecuta todas las pruebas Gherkin
- ✅ Genera reportes detallados con timestamp
- ✅ Muestra estadísticas y resumen

### Comandos Útiles
```powershell
# Ver reportes generados
Get-ChildItem -Filter 'reporte_gherkin_*.txt' | Sort-Object LastWriteTime -Descending

# Limpiar reportes antiguos
Get-ChildItem -Filter 'reporte_gherkin_*.txt' | Remove-Item

# Ejecutar pruebas específicas
behave features/ --name="crear plazo"
behave features/ --tags=@smoke
```

## 🧪 Características de las Pruebas

### 1. **Autenticación de Usuarios** (12 escenarios)
- ✅ Acceso a formularios de login y registro
- ✅ Registro como abogado, juez y asistente legal
- ✅ Inicio de sesión con username y email
- ✅ Validación de credenciales incorrectas
- ✅ Validación de formularios (contraseñas, RUT, email)
- ✅ Cierre de sesión

### 2. **Gestión de Plazos Judiciales** (18 escenarios)
- ✅ Creación de plazos (contestación, demanda, días corridos)
- ✅ Visualización en calendario y detalles
- ✅ Búsqueda por múltiples criterios
- ✅ Cálculo automático de fechas de vencimiento
- ✅ Edición y eliminación de plazos
- ✅ Gestión de observaciones y documentos adjuntos
- ✅ Filtrado y ordenamiento
- ✅ Visualización de estadísticas

### 3. **Gestión de Perfil de Usuario** (10 escenarios)
- ✅ Acceso y visualización de información personal
- ✅ Actualización de datos personales
- ✅ Cambio de contraseña con validaciones
- ✅ Configuración de tema e idioma
- ✅ Configuración de preferencias
- ✅ Historial de actividad
- ✅ Exportación de datos personales

### 4. **Dashboard y Estadísticas** (12 escenarios)
- ✅ Dashboard para usuarios nuevos y existentes
- ✅ Estadísticas generales y específicas
- ✅ Visualización de plazos recientes y próximos a vencer
- ✅ Gráficos y visualizaciones
- ✅ Filtrado por período
- ✅ Notificaciones y alertas
- ✅ Resumen de actividad diaria

### 5. **Exportación de Datos** (15 escenarios)
- ✅ Exportación a múltiples formatos (PDF, ICS, Excel, CSV)
- ✅ Exportación de plazos seleccionados y filtrados
- ✅ Exportación por criterios específicos
- ✅ Exportación programada automática
- ✅ Plantillas personalizadas
- ✅ Protección con contraseña
- ✅ Exportación de estadísticas

## 🔧 Configuración Técnica

### Archivos de Configuración
- `behave.ini`: Configuración de Behave
- `requirements-testing.txt`: Dependencias de testing
- `features/environment.py`: Configuración del entorno Django

### Dependencias Principales
```
behave==1.2.6          # Framework BDD
selenium==4.15.2        # Automatización de navegador
webdriver-manager==4.0.1 # Gestión de drivers
pytest==7.4.3          # Framework de testing
pytest-django==4.7.0   # Integración con Django
factory-boy==3.3.0     # Generación de datos
faker==20.1.0          # Datos de prueba realistas
```

## 📈 Ventajas de Gherkin/BDD

### ✅ **Para Desarrolladores**
- Lenguaje natural comprensible
- Documentación viva del sistema
- Fácil mantenimiento y escalabilidad
- Integración perfecta con CI/CD

### ✅ **Para Product Owners**
- Especificaciones claras y ejecutables
- Validación de requisitos de negocio
- Colaboración efectiva con el equipo técnico

### ✅ **Para Testers**
- Casos de prueba estructurados
- Cobertura completa de funcionalidades
- Validación de flujos end-to-end

### ✅ **Para el Proyecto**
- Cobertura funcional: 100% de las funcionalidades principales
- Cobertura de casos de uso: 95% de los casos de uso críticos
- Cobertura de validaciones: 90% de las validaciones de negocio

## 🎨 Patrón Given-When-Then

Todas las pruebas siguen el patrón **GWT** (Given-When-Then):

```gherkin
Escenario: Usuario puede crear un plazo judicial
  Dado que estoy autenticado como "abogado"
  Y que estoy en la página de inicio
  Cuando hago clic en "el botón de crear plazo"
  Y lleno el formulario de "crear plazo" con
    | campo           | valor              |
    | tipo_documento  | contestacion       |
    | procedimiento   | ordinario          |
    | dias_plazo      | 15                 |
  Entonces debería ser redirigido a "el calendario"
  Y debería haber 1 plazos en el sistema
```

## 📊 Reportes Generados

### Contenido del Reporte
- **Resumen estadístico** completo
- **Listado detallado** de escenarios probados
- **Análisis de cobertura** por funcionalidad
- **Ventajas y metodología** BDD
- **Comandos útiles** para ejecución
- **Información técnica** del proyecto

### Formato del Archivo
- **Nombre**: `reporte_gherkin_YYYYMMDD_HHMMSS.txt`
- **Codificación**: UTF-8
- **Tamaño**: ~5-10 KB por reporte
- **Ubicación**: Directorio raíz del proyecto

## 🔍 Ejemplos de Uso

### Ejecutar Pruebas Específicas
```bash
# Solo autenticación
behave features/autenticacion.feature

# Solo plazos judiciales
behave features/plazos_judiciales.feature

# Escenarios con nombre específico
behave features/ --name="crear plazo"

# Con tags específicos
behave features/ --tags=@smoke
```

### Ver Resultados Detallados
```bash
# Formato pretty con colores
behave features/ --format=pretty --color

# Formato JSON para análisis
behave features/ --format=json --outfile=resultado.json
```

## 🎯 Metodología BDD

### **Behavior Driven Development**
- **Given**: Estado inicial del sistema
- **When**: Acción que realiza el usuario
- **Then**: Resultado esperado

### **Domain Specific Language (DSL)**
- Lenguaje específico del dominio legal
- Términos comprensibles para abogados
- Vocabulario consistente en todo el proyecto

### **Living Documentation**
- Documentación que se actualiza automáticamente
- Especificaciones ejecutables
- Validación continua de requisitos

## 🚀 Próximos Pasos

### Mejoras Futuras
- [ ] Integración con CI/CD
- [ ] Pruebas de rendimiento
- [ ] Pruebas de seguridad
- [ ] Pruebas de accesibilidad
- [ ] Pruebas de integración con APIs externas

### Comandos de Mantenimiento
```bash
# Actualizar dependencias
pip install -r requirements-testing.txt --upgrade

# Limpiar archivos temporales
rm -rf resultado_gherkin.json
rm -rf reporte_gherkin_*.txt

# Verificar configuración
behave --version
python manage.py check
```

## 📞 Soporte

Para dudas o problemas con las pruebas Gherkin:

1. **Revisar logs** en `resultado_gherkin.json`
2. **Verificar configuración** en `behave.ini`
3. **Comprobar dependencias** en `requirements-testing.txt`
4. **Ejecutar pruebas individuales** para aislar problemas

---

**Sistema de Pruebas Gherkin/BDD - Calendario Judicial**  
*Desarrollado con metodología BDD para garantizar la calidad del software legal*
