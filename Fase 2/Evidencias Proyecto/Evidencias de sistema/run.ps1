# Script ultra simple para iniciar el servidor
Write-Host "Iniciando Calendario Judicial..." -ForegroundColor Green

# Activar entorno virtual
if (Test-Path "venv\Scripts\Activate.ps1") {
    & ".\venv\Scripts\Activate.ps1"
}

# Arreglar campos NULL antes de migraciones
Write-Host "Arreglando campos NULL..." -ForegroundColor Yellow
python fix_migrations.py

# Aplicar migraciones
Write-Host "Aplicando migraciones..." -ForegroundColor Yellow
python manage.py makemigrations --settings=calendario_judicial.settings_dev
python manage.py migrate --settings=calendario_judicial.settings_dev

# Cargar datos
if (Test-Path "cargar_todos_codigos.py") {
    Write-Host "Cargando datos..." -ForegroundColor Yellow
    python cargar_todos_codigos.py
}

# Iniciar servidor
Write-Host ""
Write-Host "Servidor iniciado en http://localhost:8000" -ForegroundColor Green
Write-Host "Presiona Ctrl+C para detener" -ForegroundColor Yellow
Write-Host ""

python manage.py runserver --settings=calendario_judicial.settings_dev
