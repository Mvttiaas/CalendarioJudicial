# Script para cargar códigos del CPC automáticamente
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "CARGA AUTOMÁTICA DE CÓDIGOS DEL CÓDIGO DE PROCEDIMIENTO CIVIL" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# Activar entorno virtual
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "Activando entorno virtual..." -ForegroundColor Green
    & "venv\Scripts\Activate.ps1"
} else {
    Write-Host "ERROR: No se encontró el entorno virtual" -ForegroundColor Red
    exit 1
}

# Mostrar opciones
Write-Host "`nOpciones disponibles:" -ForegroundColor Yellow
Write-Host "1. Cargar todos los códigos" -ForegroundColor White
Write-Host "2. Cargar solo códigos de procedimiento ordinario" -ForegroundColor White
Write-Host "3. Cargar solo códigos de procedimiento ejecutivo" -ForegroundColor White
Write-Host "4. Cargar solo códigos de recursos" -ForegroundColor White
Write-Host "5. Limpiar y recargar todos los códigos" -ForegroundColor White
Write-Host "6. Modo dry-run (solo mostrar qué se cargaría)" -ForegroundColor White

# Solicitar opción
$opcion = Read-Host "`nSelecciona una opción (1-6)"

switch ($opcion) {
    "1" {
        Write-Host "`nCargando todos los códigos del CPC..." -ForegroundColor Yellow
        python manage.py cargar_cpc_automatico
    }
    "2" {
        Write-Host "`nCargando códigos de procedimiento ordinario..." -ForegroundColor Yellow
        python manage.py cargar_cpc_automatico --tipo-procedimiento ordinario
    }
    "3" {
        Write-Host "`nCargando códigos de procedimiento ejecutivo..." -ForegroundColor Yellow
        python manage.py cargar_cpc_automatico --tipo-procedimiento ejecutivo
    }
    "4" {
        Write-Host "`nCargando códigos de recursos..." -ForegroundColor Yellow
        python manage.py cargar_cpc_automatico --tipo-documento recurso_apelacion
    }
    "5" {
        Write-Host "`nLimpiando y recargando todos los códigos..." -ForegroundColor Yellow
        python manage.py cargar_cpc_automatico --limpiar
    }
    "6" {
        Write-Host "`nModo dry-run - mostrando qué se cargaría..." -ForegroundColor Yellow
        python manage.py cargar_cpc_automatico --dry-run
    }
    default {
        Write-Host "`nOpción inválida. Cargando todos los códigos por defecto..." -ForegroundColor Red
        python manage.py cargar_cpc_automatico
    }
}

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nCÓDIGOS CARGADOS EXITOSAMENTE" -ForegroundColor Green
} else {
    Write-Host "`nERROR AL CARGAR CÓDIGOS" -ForegroundColor Red
}

Write-Host "`nPresiona Enter para continuar..." -ForegroundColor Gray
Read-Host
