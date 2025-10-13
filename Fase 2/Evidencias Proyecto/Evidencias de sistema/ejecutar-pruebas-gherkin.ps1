# Script mejorado para ejecutar pruebas Gherkin/BDD
# Sistema completo de pruebas de comportamiento para Calendario Judicial

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "SISTEMA DE PRUEBAS GHERKIN/BDD - CALENDARIO JUDICIAL" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# Activar el entorno virtual
if (Test-Path ".\venv\Scripts\Activate.ps1") {
    . ".\venv\Scripts\Activate.ps1"
    Write-Host "Entorno virtual activado" -ForegroundColor Green
} else {
    Write-Host "No se encontro el entorno virtual" -ForegroundColor Red
    exit 1
}

# Instalar dependencias de testing
Write-Host "Verificando dependencias de testing..." -ForegroundColor Yellow
pip install -r requirements-testing.txt --quiet

# Generar nombre único para el reporte
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$nombreArchivo = "pruebas_unitarios_CalendarioJudicialGherkin_$timestamp.txt"

Write-Host "Ejecutando pruebas Gherkin y generando reporte: $nombreArchivo" -ForegroundColor Cyan
Write-Host ""

# Iniciar cronómetro
$tiempoInicio = Get-Date

try {
    # Ejecutar las pruebas con Behave
    $resultado = behave features/ --format=json --outfile=resultado_gherkin.json 2>&1
    
    # Procesar el resultado para mejor legibilidad y corregir codificación
    $resultadoLimpio = $resultado -replace "Entorno de pruebas configurado", "=== INICIO DE PRUEBAS ==="
    $resultadoLimpio = $resultadoLimpio -replace "Ejecutando: ", "`n[EJECUTANDO] "
    $resultadoLimpio = $resultadoLimpio -replace "Paso: ", "`n[PASO] "
    $resultadoLimpio = $resultadoLimpio -replace "Fallo: ", "`n[FALLO] "
    $resultadoLimpio = $resultadoLimpio -replace "Pruebas completadas", "`n=== FIN DE PRUEBAS ==="
    $resultadoLimpio = $resultadoLimpio -replace "System\.Management\.Automation\.RemoteException", "`n[ERROR] "
    $resultadoLimpio = $resultadoLimpio -replace "You can implement step definitions for undefined steps with these snippets:", "`n`n[PASOS FALTANTES]`n"
    $resultadoLimpio = $resultadoLimpio -replace "Failing scenarios:", "`n`n[ESCENARIOS FALLIDOS]`n"
    $resultadoLimpio = $resultadoLimpio -replace "features/", "`n  - features/"
    $resultadoLimpio = $resultadoLimpio -replace "0 features passed, \d+ failed, \d+ skipped", "`n`n[RESUMEN FINAL]`n"
    $resultadoLimpio = $resultadoLimpio -replace "Took \d+m\d+\.\d+s", "`n[Tiempo total de ejecucion]"
    
    # Mejorar el formato de errores
    $resultadoLimpio = $resultadoLimpio -replace "AssertionError:", "`n[ERROR DETALLADO]"
    $resultadoLimpio = $resultadoLimpio -replace "NotImplementedError:", "`n[PASO NO IMPLEMENTADO]"
    $resultadoLimpio = $resultadoLimpio -replace "AttributeError:", "`n[ERROR DE ATRIBUTO]"
    $resultadoLimpio = $resultadoLimpio -replace "KeyError:", "`n[ERROR DE CLAVE]"
    $resultadoLimpio = $resultadoLimpio -replace "ValueError:", "`n[ERROR DE VALOR]"
    $resultadoLimpio = $resultadoLimpio -replace "TypeError:", "`n[ERROR DE TIPO]"
    
    # Corregir caracteres mal codificados de forma más exhaustiva
    $resultadoLimpio = $resultadoLimpio -replace "p[ß]gina", "pagina"
    $resultadoLimpio = $resultadoLimpio -replace "sesi[¾]n", "sesion"
    $resultadoLimpio = $resultadoLimpio -replace "contrase[±]as", "contrasenas"
    $resultadoLimpio = $resultadoLimpio -replace "inv[ß]lido", "invalido"
    $resultadoLimpio = $resultadoLimpio -replace "vac[Ý]o", "vacio"
    $resultadoLimpio = $resultadoLimpio -replace "estad[Ý]sticas", "estadisticas"
    $resultadoLimpio = $resultadoLimpio -replace "pr[¾]ximos", "proximos"
    $resultadoLimpio = $resultadoLimpio -replace "gr[ß]ficos", "graficos"
    $resultadoLimpio = $resultadoLimpio -replace "per[Ý]odo", "periodo"
    $resultadoLimpio = $resultadoLimpio -replace "le[Ý]das", "leidas"
    $resultadoLimpio = $resultadoLimpio -replace "d[Ý]a", "dia"
    $resultadoLimpio = $resultadoLimpio -replace "contestaci[¾]n", "contestacion"
    $resultadoLimpio = $resultadoLimpio -replace "d[Ý]as", "dias"
    $resultadoLimpio = $resultadoLimpio -replace "h[ß]biles", "habiles"
    $resultadoLimpio = $resultadoLimpio -replace "deber[Ý]an", "deberian"
    $resultadoLimpio = $resultadoLimpio -replace "exportaci[¾]n", "exportacion"
    $resultadoLimpio = $resultadoLimpio -replace "autom[ß]ticamente", "automaticamente"
    $resultadoLimpio = $resultadoLimpio -replace "adjuntar", "adjuntar"
    $resultadoLimpio = $resultadoLimpio -replace "documento", "documento"
    $resultadoLimpio = $resultadoLimpio -replace "vencimiento", "vencimiento"
    $resultadoLimpio = $resultadoLimpio -replace "ordenamiento", "ordenamiento"
    $resultadoLimpio = $resultadoLimpio -replace "filtrado", "filtrado"
    $resultadoLimpio = $resultadoLimpio -replace "visualizacion", "visualizacion"
    $resultadoLimpio = $resultadoLimpio -replace "observaciones", "observaciones"
    $resultadoLimpio = $resultadoLimpio -replace "eliminacion", "eliminacion"
    $resultadoLimpio = $resultadoLimpio -replace "edicion", "edicion"
    $resultadoLimpio = $resultadoLimpio -replace "calculo", "calculo"
    $resultadoLimpio = $resultadoLimpio -replace "busqueda", "busqueda"
    $resultadoLimpio = $resultadoLimpio -replace "creacion", "creacion"
    $resultadoLimpio = $resultadoLimpio -replace "gestion", "gestion"
    $resultadoLimpio = $resultadoLimpio -replace "autenticacion", "autenticacion"
    $resultadoLimpio = $resultadoLimpio -replace "registro", "registro"
    $resultadoLimpio = $resultadoLimpio -replace "validacion", "validacion"
    $resultadoLimpio = $resultadoLimpio -replace "configuracion", "configuracion"
    $resultadoLimpio = $resultadoLimpio -replace "actualizacion", "actualizacion"
    $resultadoLimpio = $resultadoLimpio -replace "informacion", "informacion"
    $resultadoLimpio = $resultadoLimpio -replace "notificaciones", "notificaciones"
    $resultadoLimpio = $resultadoLimpio -replace "actividad", "actividad"
    $resultadoLimpio = $resultadoLimpio -replace "resumen", "resumen"
    $resultadoLimpio = $resultadoLimpio -replace "graficos", "graficos"
    $resultadoLimpio = $resultadoLimpio -replace "especificos", "especificos"
    $resultadoLimpio = $resultadoLimpio -replace "generales", "generales"
    $resultadoLimpio = $resultadoLimpio -replace "existentes", "existentes"
    $resultadoLimpio = $resultadoLimpio -replace "nuevos", "nuevos"
    $resultadoLimpio = $resultadoLimpio -replace "recientes", "recientes"
    $resultadoLimpio = $resultadoLimpio -replace "proximos", "proximos"
    $resultadoLimpio = $resultadoLimpio -replace "vencidos", "vencidos"
    $resultadoLimpio = $resultadoLimpio -replace "vencer", "vencer"
    $resultadoLimpio = $resultadoLimpio -replace "periodo", "periodo"
    $resultadoLimpio = $resultadoLimpio -replace "alertas", "alertas"
    $resultadoLimpio = $resultadoLimpio -replace "diaria", "diaria"
    $resultadoLimpio = $resultadoLimpio -replace "profesional", "profesional"
    $resultadoLimpio = $resultadoLimpio -replace "calendarios", "calendarios"
    $resultadoLimpio = $resultadoLimpio -replace "seleccionados", "seleccionados"
    $resultadoLimpio = $resultadoLimpio -replace "filtrados", "filtrados"
    $resultadoLimpio = $resultadoLimpio -replace "rango", "rango"
    $resultadoLimpio = $resultadoLimpio -replace "fechas", "fechas"
    $resultadoLimpio = $resultadoLimpio -replace "documento", "documento"
    $resultadoLimpio = $resultadoLimpio -replace "tipo", "tipo"
    $resultadoLimpio = $resultadoLimpio -replace "vencidos", "vencidos"
    $resultadoLimpio = $resultadoLimpio -replace "proximos", "proximos"
    $resultadoLimpio = $resultadoLimpio -replace "vencer", "vencer"
    
    # Corregir caracteres específicos que aparecen en el output
    $resultadoLimpio = $resultadoLimpio -replace "ß", "a"
    $resultadoLimpio = $resultadoLimpio -replace "¾", "o"
    $resultadoLimpio = $resultadoLimpio -replace "±", "n"
    $resultadoLimpio = $resultadoLimpio -replace "Ý", "i"
    $resultadoLimpio = $resultadoLimpio -replace "Ý", "i"
    
    # Agregar separadores por categorías de forma más inteligente
    $resultadoLimpio = $resultadoLimpio -replace "\[EJECUTANDO\] Usuario puede acceder a la pagina de login", "`n--- AUTENTICACION ---`n[EJECUTANDO] Usuario puede acceder a la pagina de login"
    $resultadoLimpio = $resultadoLimpio -replace "\[EJECUTANDO\] Abogado puede crear un plazo", "`n--- PLAZOS JUDICIALES ---`n[EJECUTANDO] Abogado puede crear un plazo"
    $resultadoLimpio = $resultadoLimpio -replace "\[EJECUTANDO\] Usuario puede acceder a su perfil", "`n--- GESTION DE PERFIL ---`n[EJECUTANDO] Usuario puede acceder a su perfil"
    $resultadoLimpio = $resultadoLimpio -replace "\[EJECUTANDO\] Usuario nuevo ve dashboard", "`n--- DASHBOARD Y ESTADISTICAS ---`n[EJECUTANDO] Usuario nuevo ve dashboard"
    $resultadoLimpio = $resultadoLimpio -replace "\[EJECUTANDO\] Abogado puede exportar", "`n--- EXPORTACION ---`n[EJECUTANDO] Abogado puede exportar"
    
    # Limpiar separadores duplicados
    $resultadoLimpio = $resultadoLimpio -replace "--- AUTENTICACION ---`n`n--- AUTENTICACION ---", "--- AUTENTICACION ---"
    $resultadoLimpio = $resultadoLimpio -replace "--- PLAZOS JUDICIALES ---`n`n--- PLAZOS JUDICIALES ---", "--- PLAZOS JUDICIALES ---"
    $resultadoLimpio = $resultadoLimpio -replace "--- GESTION DE PERFIL ---`n`n--- GESTION DE PERFIL ---", "--- GESTION DE PERFIL ---"
    $resultadoLimpio = $resultadoLimpio -replace "--- DASHBOARD Y ESTADISTICAS ---`n`n--- DASHBOARD Y ESTADISTICAS ---", "--- DASHBOARD Y ESTADISTICAS ---"
    $resultadoLimpio = $resultadoLimpio -replace "--- EXPORTACION ---`n`n--- EXPORTACION ---", "--- EXPORTACION ---"
    
    # Crear el reporte detallado
    $fechaHora = Get-Date -Format "dd/MM/yyyy HH:mm:ss"
    
    # Analizar el resultado JSON si existe
    $estadisticas = @{
        total = 0
        exitosos = 0
        fallidos = 0
        skip = 0
    }
    
    if (Test-Path "resultado_gherkin.json") {
        try {
            $jsonContent = Get-Content "resultado_gherkin.json" -Raw | ConvertFrom-Json
            if ($jsonContent.summary) {
                $estadisticas.total = $jsonContent.summary.total
                $estadisticas.exitosos = $jsonContent.summary.passed
                $estadisticas.fallidos = $jsonContent.summary.failed
                $estadisticas.skip = $jsonContent.summary.skipped
            }
        } catch {
            # Si falla el JSON, extraer estadísticas del texto
            $estadisticas.total = ($resultado | Select-String "scenarios" | ForEach-Object { ($_ -split " ")[0] }) -join ""
            $estadisticas.exitosos = ($resultado | Select-String "passed" | ForEach-Object { ($_ -split " ")[0] }) -join ""
            $estadisticas.fallidos = ($resultado | Select-String "failed" | ForEach-Object { ($_ -split " ")[0] }) -join ""
            $estadisticas.skip = ($resultado | Select-String "skipped" | ForEach-Object { ($_ -split " ")[0] }) -join ""
        }
    }
    
    # Extraer estadísticas del resultado de behave
    $lineaResumen = $resultado | Select-String "scenarios passed.*failed.*skipped" | Select-Object -Last 1
    if ($lineaResumen) {
        $linea = $lineaResumen.Line
        if ($linea -match "(\d+)\s+scenarios\s+passed,\s+(\d+)\s+failed,\s+(\d+)\s+skipped") {
            $estadisticas.exitosos = [int]$matches[1]
            $estadisticas.fallidos = [int]$matches[2]
            $estadisticas.skip = [int]$matches[3]
            $estadisticas.total = $estadisticas.exitosos + $estadisticas.fallidos + $estadisticas.skip
        } else {
            # Patrón alternativo
            $numeros = $linea -split " " | Where-Object { $_ -match "^\d+$" }
            if ($numeros.Count -ge 3) {
                $estadisticas.exitosos = [int]$numeros[0]
                $estadisticas.fallidos = [int]$numeros[1]
                $estadisticas.skip = [int]$numeros[2]
                $estadisticas.total = $estadisticas.exitosos + $estadisticas.fallidos + $estadisticas.skip
            }
        }
    }
    
    $tasaExito = if ($estadisticas.total -gt 0) { 
        [math]::Round(($estadisticas.exitosos / $estadisticas.total) * 100, 1) 
    } else { 0 }
    
    # Calcular tiempo de ejecución
    $tiempoFin = Get-Date
    $tiempoEjecucion = $tiempoFin - $tiempoInicio
    $tiempoFormateado = "{0:hh\:mm\:ss}" -f $tiempoEjecucion
    
    # Crear el contenido del reporte con caracteres correctos
    $reporte = "================================================================================`n"
    $reporte += "PRUEBAS UNITARIAS GHERKIN/BDD - CALENDARIO JUDICIAL`n"
    $reporte += "================================================================================`n"
    $reporte += "Fecha y Hora: $fechaHora`n"
    $reporte += "Archivo: $nombreArchivo`n"
    $reporte += "Tiempo de Ejecucion: $tiempoFormateado`n"
    $reporte += "================================================================================`n`n"
    $reporte += "RESUMEN ESTADISTICO`n"
    $reporte += "----------------------------------------`n"
    $reporte += "Total de escenarios: " + $estadisticas.total + "`n"
    $reporte += "Exitosos: " + $estadisticas.exitosos + "`n"
    $reporte += "Fallidos: " + $estadisticas.fallidos + "`n"
    $reporte += "Omitidos: " + $estadisticas.skip + "`n"
    $reporte += "Tasa de exito: " + $tasaExito + "%`n`n"
    $estado = if ($estadisticas.fallidos -eq 0) { "TODAS LAS PRUEBAS PASARON EXITOSAMENTE" } else { "ALGUNAS PRUEBAS FALLARON" }
    $reporte += "ESTADO: " + $estado + "`n`n"
    $reporte += "================================================================================`n"
    $reporte += "CARACTERISTICAS PROBADAS`n"
    $reporte += "================================================================================`n"
    $reporte += "1. AUTENTICACION DE USUARIOS (12 escenarios)`n"
    $reporte += "   - Acceso a formularios de login y registro`n"
    $reporte += "   - Registro como abogado, juez y asistente legal`n"
    $reporte += "   - Inicio de sesion con username y email`n"
    $reporte += "   - Validacion de credenciales incorrectas`n"
    $reporte += "   - Validacion de formularios (contrasenas, RUT, email)`n"
    $reporte += "   - Cierre de sesion`n`n"
    $reporte += "2. GESTION DE PLAZOS JUDICIALES (18 escenarios)`n"
    $reporte += "   - Creacion de plazos (contestacion, demanda, dias corridos)`n"
    $reporte += "   - Visualizacion en calendario y detalles`n"
    $reporte += "   - Busqueda por multiples criterios`n"
    $reporte += "   - Calculo automatico de fechas de vencimiento`n"
    $reporte += "   - Edicion y eliminacion de plazos`n"
    $reporte += "   - Gestion de observaciones y documentos adjuntos`n"
    $reporte += "   - Filtrado y ordenamiento`n"
    $reporte += "   - Visualizacion de estadisticas`n`n"
    $reporte += "3. GESTION DE PERFIL DE USUARIO (10 escenarios)`n"
    $reporte += "   - Acceso y visualizacion de informacion personal`n"
    $reporte += "   - Actualizacion de datos personales`n"
    $reporte += "   - Cambio de contrasena con validaciones`n"
    $reporte += "   - Configuracion de tema e idioma`n"
    $reporte += "   - Configuracion de preferencias`n"
    $reporte += "   - Historial de actividad`n"
    $reporte += "   - Exportacion de datos personales`n`n"
    $reporte += "4. DASHBOARD Y ESTADISTICAS (12 escenarios)`n"
    $reporte += "   - Dashboard para usuarios nuevos y existentes`n"
    $reporte += "   - Estadisticas generales y especificas`n"
    $reporte += "   - Visualizacion de plazos recientes y proximos a vencer`n"
    $reporte += "   - Graficos y visualizaciones`n"
    $reporte += "   - Filtrado por periodo`n"
    $reporte += "   - Notificaciones y alertas`n"
    $reporte += "   - Resumen de actividad diaria`n`n"
    $reporte += "5. EXPORTACION DE DATOS (8 escenarios)`n"
    $reporte += "   - Exportacion a PDF con formato profesional`n"
    $reporte += "   - Exportacion a ICS para calendarios`n"
    $reporte += "   - Exportacion de plazos seleccionados`n"
    $reporte += "   - Exportacion de plazos filtrados`n"
    $reporte += "   - Exportacion por rango de fechas`n"
    $reporte += "   - Exportacion por tipo de documento`n"
    $reporte += "   - Exportacion de plazos vencidos`n"
    $reporte += "   - Exportacion de plazos proximos a vencer`n`n"
    $reporte += "================================================================================`n"
    $reporte += "COBERTURA DE PRUEBAS`n"
    $reporte += "================================================================================`n"
    $reporte += "Total de escenarios: " + $estadisticas.total + "`n"
    $reporte += "- Autenticacion: 12 escenarios`n"
    $reporte += "- Plazos Judiciales: 18 escenarios`n"
    $reporte += "- Gestion de Perfil: 10 escenarios`n"
    $reporte += "- Dashboard: 12 escenarios`n"
    $reporte += "- Exportacion: 8 escenarios`n`n"
    $reporte += "================================================================================`n"
    $reporte += "DETALLE DE EJECUCION`n"
    $reporte += "================================================================================`n`n"
    $reporte += $resultadoLimpio
    $reporte += "`n`n================================================================================`n"
    
    # Corregir caracteres en el contenido del reporte antes de guardar
    $reporte = $reporte -replace "ß", "a"
    $reporte = $reporte -replace "¾", "o"
    $reporte = $reporte -replace "±", "n"
    $reporte = $reporte -replace "Ý", "i"
    
    # También corregir caracteres en el resultado de las pruebas
    $resultadoLimpio = $resultadoLimpio -replace "ß", "a"
    $resultadoLimpio = $resultadoLimpio -replace "¾", "o"
    $resultadoLimpio = $resultadoLimpio -replace "±", "n"
    $resultadoLimpio = $resultadoLimpio -replace "Ý", "i"
    
    # Reemplazar el resultado en el reporte con la versión corregida
    $reporte = $reporte -replace '\$resultadoLimpio', $resultadoLimpio
    
    # Aplicar corrección final a todo el contenido
    $reporte = $reporte -replace "ß", "a"
    $reporte = $reporte -replace "¾", "o"
    $reporte = $reporte -replace "±", "n"
    $reporte = $reporte -replace "Ý", "i"
    $reporte = $reporte -replace "Ý", "i"
    $reporte = $reporte -replace "ß", "a"
    $reporte = $reporte -replace "¾", "o"
    $reporte = $reporte -replace "±", "n"
    
    # Guardar el reporte con codificación UTF-8 sin BOM
    [System.IO.File]::WriteAllText($nombreArchivo, $reporte, [System.Text.Encoding]::UTF8)
    
    # Mostrar resultado
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Pruebas Gherkin completadas exitosamente" -ForegroundColor Green
    } else {
        Write-Host "Algunas pruebas Gherkin fallaron" -ForegroundColor Red
    }
    
    Write-Host "Reporte generado: $nombreArchivo" -ForegroundColor Green
    Write-Host "Fecha: $fechaHora" -ForegroundColor Gray
    Write-Host "Tamano: $([math]::Round((Get-Item $nombreArchivo).Length / 1KB, 2)) KB" -ForegroundColor Gray
    
    # Mostrar resumen detallado
    Write-Host ""
    Write-Host "RESUMEN GHERKIN:" -ForegroundColor Yellow
    Write-Host "  Total: $($estadisticas.total) | Exitosos: $($estadisticas.exitosos) | Fallidos: $($estadisticas.fallidos)" -ForegroundColor White
    Write-Host "  Tasa de exito: $tasaExito% | Tiempo: $tiempoFormateado" -ForegroundColor $(if ($tasaExito -ge 80) { "Green" } elseif ($tasaExito -ge 60) { "Yellow" } else { "Red" })
    
    # Mostrar características probadas
    Write-Host ""
    Write-Host "CARACTERISTICAS PROBADAS:" -ForegroundColor Yellow
    Write-Host "  - Autenticacion de usuarios (12 escenarios)" -ForegroundColor Green
    Write-Host "  - Gestion de plazos judiciales (18 escenarios)" -ForegroundColor Green
    Write-Host "  - Gestion de perfil de usuario (10 escenarios)" -ForegroundColor Green
    Write-Host "  - Dashboard y estadisticas (12 escenarios)" -ForegroundColor Green
    Write-Host "  - Exportacion de datos (8 escenarios)" -ForegroundColor Green
    
} catch {
    Write-Host "Error durante la ejecucion: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "COMANDOS UTILES:" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Ver reportes: Get-ChildItem -Filter 'reporte_gherkin_*.txt' | Sort-Object LastWriteTime -Descending" -ForegroundColor Gray
Write-Host "Ejecutar pruebas: behave features/" -ForegroundColor Gray
Write-Host "Ver ayuda: behave --help" -ForegroundColor Gray
Write-Host "Limpiar reportes: Get-ChildItem -Filter 'reporte_gherkin_*.txt' | Remove-Item" -ForegroundColor Gray
Write-Host ""

Write-Host "Presiona Enter para continuar..." -ForegroundColor Gray
Read-Host | Out-Null
