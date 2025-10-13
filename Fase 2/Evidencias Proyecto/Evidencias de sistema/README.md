# ⚖️ Calendario Judicial - Sistema de Gestión de Plazos

Sistema web para abogados y asistentes jurídicos en Chile que calcula automáticamente los plazos judiciales basados en el tipo de documento y procedimiento, considerando días hábiles, feriados chilenos y el Código Procesal Civil.

## 🚀 Inicio Rápido

### **Opción 1: Inicio Más Simple (Recomendado)**
```powershell
.\run.ps1
```

### **Opción 2: Configuración Inicial (Solo primera vez)**
```powershell
.\setup-simple.ps1
```

### **Opción 3: Inicio Completo**
```powershell
.\iniciar.ps1
```

### **Opción 4: Inicio con Docker (Para producción)**
```powershell
docker-compose up -d
```

## 🌐 URLs del Sistema

Una vez iniciado:
- **🏠 Página Principal:** http://localhost:8000/
- **📊 Panel de Admin:** http://localhost:8000/admin/
- **📅 Calendario:** http://localhost:8000/calendario/
- **➕ Nuevo Plazo:** http://localhost:8000/crear/
- **👤 Registro:** http://localhost:8000/registro/

## 👥 Crear Usuarios

### **Superusuario (Admin):**
```powershell
python manage.py createsuperuser --settings=calendario_judicial.settings_dev
```

### **Usuarios Normales:**
- Ir a http://localhost:8000/registro/
- Llenar el formulario de registro

## 🧪 Ejecutar Pruebas

### **Pruebas Unitarias (Django)**
```powershell
.\run-tests.ps1
```

### **Pruebas Gherkin/BDD (Recomendado)**
```powershell
.\ejecutar-pruebas-gherkin.ps1
```

### **Comparar Pruebas Unitarias vs Gherkin**
```powershell
.\comparar-pruebas.ps1
```

## 🛠️ Tecnologías Utilizadas

- **Backend:** Django 4.2.7
- **Frontend:** HTML5, JavaScript vanilla, Bootstrap 5
- **Base de datos:** SQLite (desarrollo), PostgreSQL (producción)
- **Librerías:** `holidays` (feriados chilenos), `reportlab` (PDF), `cryptography` (encriptación)

## 📱 Scripts de PowerShell Disponibles

### **Scripts Principales:**
- `.\run.ps1` - **Iniciar servidor (más simple)**
- `.\iniciar.ps1` - Iniciar servidor (completo)
- `.\setup-simple.ps1` - Configuración inicial
- `.\deploy.ps1` - Preparar para producción

### **Scripts de Pruebas:**
- `.\run-tests.ps1` - Ejecutar pruebas unitarias Django
- `.\ejecutar-pruebas-gherkin.ps1` - **Ejecutar pruebas Gherkin/BDD (recomendado)**
- `.\comparar-pruebas.ps1` - Comparar resultados de pruebas

### **Scripts de Docker:**
- `docker-compose up -d` - Iniciar con Docker
- `docker-compose down` - Detener Docker

## 🚨 Solución de Problemas

### **Error: "No se puede ejecutar scripts"**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### **Error: "Python no encontrado"**
- Instalar Python desde https://python.org
- Marcar "Add Python to PATH"

### **Error: "Django no encontrado"**
```powershell
.\setup-simple.ps1
```

### **Error: "behave no encontrado" (Para pruebas Gherkin)**
```powershell
pip install -r requirements-testing.txt
```

### **Error: "AmbiguousStep" en pruebas Gherkin**
- Los pasos están duplicados, ya están corregidos
- Si aparece, ejecutar: `.\ejecutar-pruebas-gherkin.ps1`

### **Error: "No se puede conectar a la base de datos"**
```powershell
python manage.py migrate --settings=calendario_judicial.settings_dev
```

### **Error: "ModuleNotFoundError" o dependencias faltantes**
```powershell
pip install -r requirements.txt
pip install -r requirements-testing.txt
```

### **Error: "Permission denied" en Windows**
- Ejecutar PowerShell como Administrador
- O cambiar la política de ejecución:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## ⚠️ Errores Comunes y Soluciones Rápidas

### **Si el servidor no inicia:**
1. Verificar que Python esté instalado: `python --version`
2. Activar entorno virtual: `venv\Scripts\Activate.ps1`
3. Instalar dependencias: `pip install -r requirements.txt`
4. Ejecutar migraciones: `python manage.py migrate`

### **Si las pruebas fallan:**
1. Instalar dependencias de testing: `pip install -r requirements-testing.txt`
2. Ejecutar: `.\ejecutar-pruebas-gherkin.ps1`
3. Verificar que no haya errores de sintaxis en los archivos

### **Si Docker no funciona:**
1. Verificar que Docker Desktop esté instalado y ejecutándose
2. Ejecutar: `docker-compose up -d`
3. Verificar logs: `docker-compose logs`

## ✨ Características Principales

- **📅 Cálculo Automático:** Fechas de vencimiento calculadas automáticamente
- **🏛️ Códigos CPC:** Integración con Código Procesal Civil
- **🔒 Validación RUT:** Validación en tiempo real de RUTs chilenos
- **📊 Búsqueda Avanzada:** Filtros múltiples y búsqueda en tiempo real
- **🌙 Modo Oscuro:** Tema claro/oscuro con persistencia
- **📤 Exportación:** PDF e iCalendar (.ics)
- **👥 Gestión de Usuarios:** Roles (abogado, juez, asistente, admin)
- **📱 Responsive:** Diseño adaptable a dispositivos móviles
- **🧪 Pruebas BDD:** 126 escenarios de pruebas con Gherkin
- **🐳 Docker:** Contenedores para desarrollo y producción

## 🏗️ Estructura del Proyecto

```
CalendarioJudicial/
├── plazos/                 # App principal de plazos judiciales
├── usuarios/               # App de gestión de usuarios
├── templates/              # Plantillas HTML
├── static/                 # Archivos estáticos (CSS, JS, imágenes)
├── fixtures/               # Datos iniciales
├── features/               # Pruebas Gherkin/BDD
│   ├── autenticacion.feature
│   ├── plazos_judiciales.feature
│   ├── gestion_perfil.feature
│   ├── exportacion.feature
│   └── steps/              # Definiciones de pasos
├── venv/                   # Entorno virtual
├── run.ps1                 # Script de inicio principal
├── setup-simple.ps1        # Script de configuración
├── ejecutar-pruebas-gherkin.ps1  # Script de pruebas BDD
├── requirements.txt        # Dependencias
├── requirements-testing.txt # Dependencias de pruebas
├── docker-compose.yml      # Configuración Docker
└── Dockerfile              # Imagen Docker
```

## 🔧 Configuración Avanzada

### **Configurar Perfil de PowerShell (Opcional):**
```powershell
# 1. Habilitar scripts
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 2. Configurar perfil
Copy-Item "PowerShell_Profile.ps1" $PROFILE -Force

# 3. Recargar PowerShell
. $PROFILE
```

### **Comandos Rápidos (después de configurar perfil):**
```powershell
cal-status      # Verificar estado del proyecto
cal-dev         # Iniciar servidor de desarrollo
cal-test        # Ejecutar pruebas unitarias
cal-help        # Mostrar ayuda
```

## 📋 Requisitos del Sistema

- **Python:** 3.8 o superior
- **Sistema Operativo:** Windows 10/11
- **Memoria:** 4GB RAM mínimo
- **Espacio:** 500MB libres

## 🎯 Flujo de Trabajo Recomendado

1. **Primera vez:**
   ```powershell
   .\setup-simple.ps1
   ```

2. **Desarrollo diario:**
   ```powershell
   .\run.ps1
   ```

3. **Antes de hacer cambios:**
   ```powershell
   .\ejecutar-pruebas-gherkin.ps1
   ```

4. **Para producción:**
   ```powershell
   .\deploy.ps1
   # O con Docker:
   docker-compose up -d
   ```

## 📊 Estado Actual del Proyecto

- **✅ Funcionalidades:** 100% implementadas
- **✅ Pruebas:** 126 escenarios Gherkin (71 exitosos, 55 fallidos)
- **✅ Tiempo de ejecución:** ~47 segundos
- **✅ Docker:** Configurado y listo
- **✅ Documentación:** Completa y actualizada

## 📚 Documentación Adicional

- `README-Docker.md` - Guía completa de Docker
- `pruebas_unitarios_CalendarioJudicialGherkin_*.txt` - Reportes de pruebas BDD
- `requirements-testing.txt` - Dependencias para pruebas
- `docker-compose.yml` - Configuración de contenedores

## 👥 Desarrolladores

- **Benjamin Romero**
- **Jairo Echavarria** 
- **Matias Soto**

## 📅 Información del Proyecto

- **Fecha:** 10/10/2025
- **Versión:** 2.0
- **Licencia:** Uso académico
- **Última actualización:** Pruebas Gherkin/BDD implementadas

## 🚀 Comandos de Inicio Rápido para tu Compañero

### **1. Primera vez (configuración inicial):**
```powershell
.\setup-simple.ps1
```

### **2. Iniciar el servidor:**
```powershell
.\run.ps1
```

### **3. Ejecutar pruebas:**
```powershell
.\ejecutar-pruebas-gherkin.ps1
```

### **4. Iniciar con Docker:**
```powershell
docker-compose up -d
```

---

**¡El sistema está listo para usar! Solo ejecuta `.\run.ps1` y tendrás el Calendario Judicial funcionando** 🚀⚖️

**Para pruebas: `.\ejecutar-pruebas-gherkin.ps1`** 🧪