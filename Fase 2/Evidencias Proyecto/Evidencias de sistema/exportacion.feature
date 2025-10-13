# language: es
# encoding: utf-8

Característica: Exportación de datos
  Como abogado
  Quiero poder exportar mis plazos judiciales
  Para generar reportes y compartir información

  Escenario: Abogado puede exportar todos los plazos a PDF
    Dado que estoy autenticado como "abogado"
    Y que tengo varios plazos judiciales creados
    Cuando hago clic en "el botón de calendario"
    Y exporto los plazos a "PDF"
    Entonces debería recibir un archivo "PDF"
    Y el archivo debería contener "todos los plazos"

  Escenario: Abogado puede exportar plazos a formato ICS
    Dado que estoy autenticado como "abogado"
    Y que tengo varios plazos judiciales creados
    Cuando hago clic en "el botón de calendario"
    Y exporto los plazos a "ICS"
    Entonces debería recibir un archivo "ICS"
    Y el archivo debería ser compatible con calendarios

  Escenario: Abogado puede exportar plazos seleccionados a PDF
    Dado que estoy autenticado como "abogado"
    Y que tengo varios plazos judiciales creados
    Cuando hago clic en "el botón de calendario"
    Y selecciono 2 plazos para exportar
    Y exporto los plazos seleccionados a "PDF"
    Entonces debería recibir un archivo "PDF"
    Y el archivo debería contener solo los 2 plazos seleccionados

  Escenario: Abogado puede exportar plazos filtrados
    Dado que estoy autenticado como "abogado"
    Y que tengo varios plazos judiciales creados
    Cuando filtro los plazos por "estado corriendo"
    Y exporto los plazos filtrados a "PDF"
    Entonces debería recibir un archivo "PDF"
    Y el archivo debería contener solo plazos corriendo

  Escenario: Abogado puede exportar plazos por rango de fechas
    Dado que estoy autenticado como "abogado"
    Y que tengo varios plazos judiciales creados
    Cuando filtro por fechas desde "2025-01-01" hasta "2025-01-31"
    Y exporto los plazos filtrados a "PDF"
    Entonces debería recibir un archivo "PDF"
    Y el archivo debería contener solo plazos de enero 2025

  Escenario: Abogado puede exportar plazos por tipo de documento
    Dado que estoy autenticado como "abogado"
    Y que tengo varios plazos judiciales creados
    Cuando filtro por "tipo de documento contestación"
    Y exporto los plazos filtrados a "PDF"
    Entonces debería recibir un archivo "PDF"
    Y el archivo debería contener solo plazos de contestación

  Escenario: Abogado puede exportar plazos vencidos
    Dado que estoy autenticado como "abogado"
    Y que tengo plazos vencidos
    Cuando filtro por "estado vencido"
    Y exporto los plazos filtrados a "PDF"
    Entonces debería recibir un archivo "PDF"
    Y el archivo debería contener solo plazos vencidos

  Escenario: Abogado puede exportar plazos próximos a vencer
    Dado que estoy autenticado como "abogado"
    Y que tengo plazos próximos a vencer
    Cuando filtro por "plazos próximos a vencer"
    Y exporto los plazos filtrados a "PDF"
    Entonces debería recibir un archivo "PDF"
    Y el archivo debería contener solo plazos próximos a vencer

  Escenario: Abogado puede exportar a Excel
    Dado que estoy autenticado como "abogado"
    Y que tengo varios plazos judiciales creados
    Cuando hago clic en "el botón de calendario"
    Y exporto los plazos a "Excel"
    Entonces debería recibir un archivo "Excel"
    Y el archivo debería contener "hojas de cálculo"

  Escenario: Abogado puede exportar a CSV
    Dado que estoy autenticado como "abogado"
    Y que tengo varios plazos judiciales creados
    Cuando hago clic en "el botón de calendario"
    Y exporto los plazos a "CSV"
    Entonces debería recibir un archivo "CSV"
    Y el archivo debería contener "datos separados por comas"

  Escenario: Abogado puede programar exportación automática
    Dado que estoy autenticado como "abogado"
    Y que tengo varios plazos judiciales creados
    Cuando hago clic en "configurar exportación automática"
    Y configuro exportación semanal a "PDF"
    Entonces la exportación debería programarse
    Y debería recibir "confirmación de programación"

  Escenario: Abogado puede exportar con plantilla personalizada
    Dado que estoy autenticado como "abogado"
    Y que tengo varios plazos judiciales creados
    Cuando selecciono "plantilla personalizada"
    Y exporto los plazos a "PDF"
    Entonces debería recibir un archivo "PDF"
    Y el archivo debería usar "la plantilla personalizada"

  Escenario: Abogado puede exportar estadísticas
    Dado que estoy autenticado como "abogado"
    Y que tengo varios plazos judiciales creados
    Cuando hago clic en "exportar estadísticas"
    Y selecciono formato "PDF"
    Entonces debería recibir un archivo "PDF"
    Y el archivo debería contener "gráficos y estadísticas"

  Escenario: Abogado puede exportar por cliente
    Dado que estoy autenticado como "abogado"
    Y que tengo plazos de diferentes clientes
    Cuando filtro por "cliente específico"
    Y exporto los plazos a "PDF"
    Entonces debería recibir un archivo "PDF"
    Y el archivo debería contener solo plazos del cliente seleccionado

  Escenario: Abogado puede exportar con contraseña
    Dado que estoy autenticado como "abogado"
    Y que tengo varios plazos judiciales creados
    Cuando selecciono "proteger con contraseña"
    Y exporto los plazos a "PDF"
    Entonces debería recibir un archivo "PDF protegido"
    Y el archivo debería requerir contraseña para abrir

  Escenario: Abogado puede exportar plazos filtrados a PDF
    Dado que estoy autenticado como "abogado"
    Y que tengo varios plazos creados
    Cuando filtro por tipo de documento "demanda"
    Y hago clic en "exportar PDF filtrados"
    Entonces debería recibir un archivo PDF
    Y la exportación debería incluir solo plazos seleccionados

  Escenario: Abogado puede exportar plazos por rango de fechas específico
    Dado que estoy autenticado como "abogado"
    Y que tengo varios plazos creados
    Cuando filtro por rango de fechas desde "2025-01-01" hasta "2025-12-31"
    Y hago clic en "exportar PDF por fechas"
    Entonces debería recibir un archivo PDF

  Escenario: Abogado puede exportar plazos vencidos
    Dado que estoy autenticado como "abogado"
    Y que tengo plazos vencidos
    Cuando filtro por estado "vencido"
    Y hago clic en "exportar PDF vencidos"
    Entonces debería recibir un archivo PDF

  Escenario: Abogado puede exportar plazos próximos a vencer
    Dado que estoy autenticado como "abogado"
    Y que tengo plazos próximos a vencer
    Cuando filtro por estado "corriendo"
    Y hago clic en "exportar PDF próximos"
    Entonces debería recibir un archivo PDF

  Escenario: Abogado puede configurar exportación automática
    Dado que estoy autenticado como "abogado"
    Cuando configuro exportación semanal
    Entonces la configuración de exportación debería guardarse

  Escenario: Abogado puede exportar con plantilla personalizada
    Dado que estoy autenticado como "abogado"
    Y que tengo varios plazos creados
    Cuando selecciono plantilla personalizada
    Y hago clic en "exportar PDF personalizado"
    Entonces debería recibir un archivo PDF

  Escenario: Abogado puede proteger exportación con contraseña específica
    Dado que estoy autenticado como "abogado"
    Y que tengo varios plazos creados
    Cuando protejo con contraseña "mi_password_123"
    Y hago clic en "exportar PDF protegido"
    Entonces debería recibir un archivo PDF
    Y la exportación debería estar protegida con contraseña

  Escenario: Abogado puede exportar plazos por rango de fechas específico
    Dado que estoy autenticado como "abogado"
    Y que tengo plazos de diferentes fechas
    Cuando hago clic en "el botón de calendario"
    Y filtro por fechas desde "2025-01-01" hasta "2025-01-31"
    Y exporto los plazos a "PDF"
    Entonces debería recibir un archivo PDF
    Y el archivo debería contener "solo plazos de enero 2025"

  Escenario: Abogado puede exportar plazos por tipo de documento
    Dado que estoy autenticado como "abogado"
    Y que tengo plazos de diferentes tipos
    Cuando hago clic en "el botón de calendario"
    Y filtro por "tipo de documento" con valor "demanda"
    Y exporto los plazos a "PDF"
    Entonces debería recibir un archivo PDF
    Y el archivo debería contener solo plazos de demanda

  Escenario: Abogado puede exportar plazos por estado específico
    Dado que estoy autenticado como "abogado"
    Y que tengo plazos en diferentes estados
    Cuando hago clic en "el botón de calendario"
    Y filtro por "estado" con valor "corriendo"
    Y exporto los plazos a "PDF"
    Entonces debería recibir un archivo PDF
    Y el archivo debería contener solo plazos corriendo

  Escenario: Abogado puede exportar plazos seleccionados manualmente
    Dado que estoy autenticado como "abogado"
    Y que tengo varios plazos creados
    Cuando hago clic en "el botón de calendario"
    Y selecciono "2" plazos para exportar
    Y exporto los plazos a "PDF"
    Entonces debería recibir un archivo PDF
    Y el archivo debería contener "solo los 2 plazos seleccionados"

  Escenario: Abogado puede exportar plazos con plantilla personalizada
    Dado que estoy autenticado como "abogado"
    Y que tengo varios plazos creados
    Cuando hago clic en "el botón de calendario"
    Y selecciono plantilla personalizada
    Y exporto los plazos a "PDF"
    Entonces debería recibir un archivo PDF
    Y el archivo debería usar "la plantilla personalizada"

  Escenario: Abogado puede exportar plazos vencidos únicamente
    Dado que estoy autenticado como "abogado"
    Y que tengo plazos vencidos
    Cuando hago clic en "el botón de calendario"
    Y filtro por "estado" con valor "vencido"
    Y exporto los plazos a "PDF"
    Entonces debería recibir un archivo PDF
    Y el archivo debería contener solo plazos vencidos

  Escenario: Abogado puede exportar plazos próximos a vencer
    Dado que estoy autenticado como "abogado"
    Y que tengo plazos próximos a vencer
    Cuando hago clic en "el botón de calendario"
    Y filtro por "estado" con valor "corriendo"
    Y exporto los plazos a "PDF"
    Entonces debería recibir un archivo PDF
    Y el archivo debería contener solo plazos próximos a vencer

  Escenario: Abogado puede exportar plazos de un cliente específico
    Dado que estoy autenticado como "abogado"
    Y que tengo plazos de diferentes clientes
    Cuando hago clic en "el botón de calendario"
    Y busco por "RUT de cliente" con valor "12345678-9"
    Y exporto los plazos a "PDF"
    Entonces debería recibir un archivo PDF
    Y el archivo debería contener "solo plazos del cliente seleccionado"

  Escenario: Abogado puede exportar plazos en formato ICS con eventos
    Dado que estoy autenticado como "abogado"
    Y que tengo varios plazos creados
    Cuando hago clic en "el botón de calendario"
    Y exporto los plazos a "ICS"
    Entonces debería recibir un archivo ICS
    Y el archivo debería ser compatible con calendarios

  Escenario: Abogado puede configurar exportación automática
    Dado que estoy autenticado como "abogado"
    Y que tengo varios plazos creados
    Cuando hago clic en "configurar exportación automática"
    Y configuro exportación semanal
    Entonces la configuración debería ser guardada
    Y debería recibir "confirmación de programación"
