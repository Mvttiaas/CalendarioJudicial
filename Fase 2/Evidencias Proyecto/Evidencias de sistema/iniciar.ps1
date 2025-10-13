# Script simple para iniciar el servidor
Write-Host "Iniciando Calendario Judicial..." -ForegroundColor Green

# Activar entorno virtual
if (Test-Path "venv\Scripts\Activate.ps1") {
    & ".\venv\Scripts\Activate.ps1"
    Write-Host "Entorno virtual activado" -ForegroundColor Green
}

# Aplicar migraciones
Write-Host "Aplicando migraciones..." -ForegroundColor Yellow
python manage.py makemigrations --settings=calendario_judicial.settings_dev
python manage.py migrate --settings=calendario_judicial.settings_dev

# Cargar datos si no existen
if (Test-Path "cargar_todos_codigos.py") {
    Write-Host "Cargando datos iniciales..." -ForegroundColor Yellow
    python cargar_todos_codigos.py
}

# Iniciar servidor
Write-Host ""
Write-Host "=================================================================================" -ForegroundColor Cyan
Write-Host "                            SERVIDOR INICIADO" -ForegroundColor Yellow
Write-Host "=================================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Servidor: http://localhost:8000" -ForegroundColor White
Write-Host "Admin: http://localhost:8000/admin/" -ForegroundColor White
Write-Host "Inicio: http://localhost:8000/" -ForegroundColor White
Write-Host ""
Write-Host "Presiona Ctrl+C para detener" -ForegroundColor Yellow
Write-Host ""

python manage.py runserver --settings=calendario_judicial.settings_dev