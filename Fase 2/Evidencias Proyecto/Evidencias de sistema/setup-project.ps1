# ================================================================================
# Script de PowerShell para configurar el proyecto desde cero
# Calendario Judicial - Sistema de Gestión de Plazos
# ================================================================================

Write-Host "=================================================================================" -ForegroundColor Cyan
Write-Host "                    CONFIGURACIÓN DEL PROYECTO CALENDARIO JUDICIAL" -ForegroundColor Yellow
Write-Host "=================================================================================" -ForegroundColor Cyan
Write-Host ""

# Verificar Python
Write-Host "1. Verificando Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python detectado: $pythonVersion" -ForegroundColor Green
    
    # Verificar versión mínima (3.8+)
    $version = [System.Version]::Parse($pythonVersion.Split(' ')[1])
    if ($version.Major -ge 3 -and $version.Minor -ge 8) {
        Write-Host "✓ Versión de Python compatible" -ForegroundColor Green
    } else {
        Write-Host "⚠ Advertencia: Se recomienda Python 3.8 o superior" -ForegroundColor Yellow
    }
} catch {
    Write-Host "✗ Error: Python no está instalado o no está en el PATH" -ForegroundColor Red
    Write-Host "  Por favor instala Python 3.8+ desde https://python.org" -ForegroundColor Yellow
    Read-Host "Presiona Enter para salir"
    exit 1
}

# Verificar pip
Write-Host ""
Write-Host "2. Verificando pip..." -ForegroundColor Yellow
try {
    $pipVersion = pip --version 2>&1
    Write-Host "✓ pip detectado: $pipVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Error: pip no está disponible" -ForegroundColor Red
    Read-Host "Presiona Enter para salir"
    exit 1
}

# Crear entorno virtual
Write-Host ""
Write-Host "3. Creando entorno virtual..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "✓ Entorno virtual ya existe" -ForegroundColor Green
} else {
    try {
        python -m venv venv
        Write-Host "✓ Entorno virtual creado" -ForegroundColor Green
    } catch {
        Write-Host "✗ Error creando entorno virtual" -ForegroundColor Red
        Read-Host "Presiona Enter para salir"
        exit 1
    }
}

# Activar entorno virtual
Write-Host ""
Write-Host "4. Activando entorno virtual..." -ForegroundColor Yellow
try {
    & ".\venv\Scripts\Activate.ps1"
    Write-Host "✓ Entorno virtual activado" -ForegroundColor Green
} catch {
    Write-Host "✗ Error activando entorno virtual" -ForegroundColor Red
    Write-Host "  Intenta ejecutar: .\venv\Scripts\Activate.ps1" -ForegroundColor Yellow
}

# Actualizar pip
Write-Host ""
Write-Host "5. Actualizando pip..." -ForegroundColor Yellow
try {
    python -m pip install --upgrade pip
    Write-Host "✓ pip actualizado" -ForegroundColor Green
} catch {
    Write-Host "⚠ Advertencia: No se pudo actualizar pip" -ForegroundColor Yellow
}

# Instalar dependencias
Write-Host ""
Write-Host "6. Instalando dependencias..." -ForegroundColor Yellow
if (Test-Path "requirements.txt") {
    try {
        pip install -r requirements.txt
        Write-Host "✓ Dependencias instaladas desde requirements.txt" -ForegroundColor Green
    } catch {
        Write-Host "⚠ Advertencia: Error instalando desde requirements.txt" -ForegroundColor Yellow
        Write-Host "  Instalando dependencias básicas..." -ForegroundColor Yellow
        
        $dependencies = @(
            "Django==4.2.7",
            "Pillow==10.0.1",
            "python-dateutil==2.8.2",
            "holidays==0.34",
            "reportlab==4.0.4",
            "cryptography==41.0.4"
        )
        
        foreach ($dep in $dependencies) {
            try {
                pip install $dep
                Write-Host "✓ $dep instalado" -ForegroundColor Green
            } catch {
                Write-Host "✗ Error instalando $dep" -ForegroundColor Red
            }
        }
    }
} else {
    Write-Host "⚠ requirements.txt no encontrado, instalando dependencias básicas..." -ForegroundColor Yellow
    
    $dependencies = @(
        "Django==4.2.7",
        "Pillow==10.0.1", 
        "python-dateutil==2.8.2",
        "holidays==0.34",
        "reportlab==4.0.4",
        "cryptography==41.0.4"
    )
    
    foreach ($dep in $dependencies) {
        try {
            pip install $dep
            Write-Host "✓ $dep instalado" -ForegroundColor Green
        } catch {
            Write-Host "✗ Error instalando $dep" -ForegroundColor Red
        }
    }
}

# Aplicar migraciones
Write-Host ""
Write-Host "7. Aplicando migraciones..." -ForegroundColor Yellow
try {
    python manage.py migrate --settings=calendario_judicial.settings_dev
    Write-Host "✓ Migraciones aplicadas" -ForegroundColor Green
} catch {
    Write-Host "✗ Error aplicando migraciones" -ForegroundColor Red
    Write-Host "  Verifica la configuración de la base de datos" -ForegroundColor Yellow
}

# Crear superusuario
Write-Host ""
Write-Host "8. Creando superusuario..." -ForegroundColor Yellow
$createSuperuser = Read-Host "¿Crear superusuario? (s/n)"
if ($createSuperuser -eq "s" -or $createSuperuser -eq "S" -or $createSuperuser -eq "y" -or $createSuperuser -eq "Y") {
    try {
        python manage.py createsuperuser --settings=calendario_judicial.settings_dev
        Write-Host "✓ Superusuario creado" -ForegroundColor Green
    } catch {
        Write-Host "⚠ Advertencia: Error creando superusuario" -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠ Superusuario no creado" -ForegroundColor Yellow
}

# Cargar datos iniciales
Write-Host ""
Write-Host "9. Cargando datos iniciales..." -ForegroundColor Yellow
if (Test-Path "cargar_todos_codigos.py") {
    try {
        python cargar_todos_codigos.py
        Write-Host "✓ Datos iniciales cargados" -ForegroundColor Green
    } catch {
        Write-Host "⚠ Advertencia: Error cargando datos iniciales" -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠ Script de datos iniciales no encontrado" -ForegroundColor Yellow
}

# Verificar configuración
Write-Host ""
Write-Host "10. Verificando configuración..." -ForegroundColor Yellow
try {
    python manage.py check --settings=calendario_judicial.settings_dev
    Write-Host "✓ Configuración verificada" -ForegroundColor Green
} catch {
    Write-Host "⚠ Advertencia: Hay problemas en la configuración" -ForegroundColor Yellow
}

# Resumen final
Write-Host ""
Write-Host "=================================================================================" -ForegroundColor Cyan
Write-Host "                            CONFIGURACIÓN COMPLETADA" -ForegroundColor Yellow
Write-Host "=================================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "✓ Proyecto configurado correctamente" -ForegroundColor Green
Write-Host ""
Write-Host "Para iniciar el servidor de desarrollo:" -ForegroundColor Yellow
Write-Host "  .\start-dev.ps1" -ForegroundColor White
Write-Host ""
Write-Host "Para ejecutar pruebas:" -ForegroundColor Yellow
Write-Host "  .\run-tests.ps1" -ForegroundColor White
Write-Host ""
Write-Host "Para crear un superusuario:" -ForegroundColor Yellow
Write-Host "  python manage.py createsuperuser --settings=calendario_judicial.settings_dev" -ForegroundColor White
Write-Host ""
Write-Host "URLs importantes:" -ForegroundColor Yellow
Write-Host "  🌐 Servidor: http://localhost:8000" -ForegroundColor White
Write-Host "  📊 Admin: http://localhost:8000/admin/" -ForegroundColor White
Write-Host "  🏠 Inicio: http://localhost:8000/" -ForegroundColor White
Write-Host ""
Write-Host "=================================================================================" -ForegroundColor Cyan

Read-Host "Presiona Enter para continuar"