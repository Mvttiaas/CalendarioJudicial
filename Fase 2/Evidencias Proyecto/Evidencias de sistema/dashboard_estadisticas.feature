# language: es
# encoding: utf-8

Característica: Dashboard y estadísticas
  Como usuario del sistema
  Quiero poder ver un dashboard con estadísticas
  Para tener una visión general de mis plazos judiciales

  Escenario: Usuario nuevo ve dashboard vacío
    Dado que estoy autenticado como "abogado"
    Y que no tengo plazos creados
    Cuando accedo al dashboard
    Entonces debería ver "Bienvenido al sistema"
    Y debería ver "No tienes plazos creados"
    Y debería ver "el botón de crear primer plazo"

  Escenario: Usuario ve estadísticas generales
    Dado que estoy autenticado como "abogado"
    Y que tengo varios plazos creados
    Cuando accedo al dashboard
    Entonces debería ver "el total de plazos"
    Y debería ver "plazos corriendo"
    Y debería ver "plazos vencidos"
    Y debería ver "plazos suspendidos"

  Escenario: Usuario ve plazos recientes
    Dado que estoy autenticado como "abogado"
    Y que tengo varios plazos creados
    Cuando accedo al dashboard
    Entonces debería ver "plazos recientes"
    Y debería ver "los últimos 5 plazos creados"

  Escenario: Usuario ve plazos próximos a vencer
    Dado que estoy autenticado como "abogado"
    Y que tengo plazos próximos a vencer
    Cuando accedo al dashboard
    Entonces debería ver "plazos próximos a vencer"
    Y los plazos deberían estar ordenados por fecha de vencimiento

  Escenario: Usuario ve plazos vencidos
    Dado que estoy autenticado como "abogado"
    Y que tengo plazos vencidos
    Cuando accedo al dashboard
    Entonces debería ver "plazos vencidos"
    Y los plazos vencidos deberían estar marcados claramente

  Escenario: Usuario puede acceder al calendario desde el dashboard
    Dado que estoy autenticado como "abogado"
    Y que accedo al dashboard
    Cuando hago clic en "ver calendario completo"
    Entonces debería ser redirigido a "el calendario"

  Escenario: Usuario puede crear un nuevo plazo desde el dashboard
    Dado que estoy autenticado como "abogado"
    Y que accedo al dashboard
    Cuando hago clic en "crear nuevo plazo"
    Entonces debería ser redirigido a "la página de crear plazo"

  Escenario: Usuario ve gráficos de estadísticas
    Dado que estoy autenticado como "abogado"
    Y que tengo varios plazos creados
    Cuando accedo al dashboard
    Entonces debería ver "gráfico de plazos por estado"
    Y debería ver "gráfico de plazos por mes"
    Y debería ver "gráfico de tipos de documento"

  Escenario: Usuario puede filtrar estadísticas por período
    Dado que estoy autenticado como "abogado"
    Y que tengo varios plazos creados
    Cuando accedo al dashboard
    Y selecciono el período "último mes"
    Entonces las estadísticas deberían mostrar solo datos del último mes

  Escenario: Usuario puede exportar estadísticas
    Dado que estoy autenticado como "abogado"
    Y que tengo varios plazos creados
    Cuando accedo al dashboard
    Y hago clic en "exportar estadísticas"
    Entonces debería recibir un archivo con "las estadísticas"
    Y el archivo debería contener "gráficos y datos"

  Escenario: Usuario ve notificaciones importantes
    Dado que estoy autenticado como "abogado"
    Y que tengo plazos próximos a vencer
    Cuando accedo al dashboard
    Entonces debería ver "notificaciones importantes"
    Y debería ver "alertas de plazos urgentes"

  Escenario: Usuario puede marcar notificaciones como leídas
    Dado que estoy autenticado como "abogado"
    Y que tengo notificaciones no leídas
    Cuando accedo al dashboard
    Y hago clic en "marcar como leído"
    Entonces las notificaciones deberían marcarse como leídas
    Y no deberían aparecer en futuras visitas

  Escenario: Usuario ve resumen de actividad del día
    Dado que estoy autenticado como "abogado"
    Y que tengo actividad del día
    Cuando accedo al dashboard
    Entonces debería ver "resumen del día"
    Y debería ver "plazos creados hoy"
    Y debería ver "plazos vencidos hoy"
    Y debería ver "plazos que vencen mañana"
