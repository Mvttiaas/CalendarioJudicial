# language: es
# encoding: utf-8

Característica: Gestión de plazos judiciales
  Como abogado
  Quiero poder crear y gestionar plazos judiciales
  Para llevar un control de mis casos legales

  Escenario: Abogado puede crear un plazo de contestación
    Dado que estoy autenticado como "abogado"
    Y que estoy en la página de inicio
    Cuando hago clic en "el botón de crear plazo"
    Y lleno el formulario de "crear plazo" con
      | campo           | valor              |
      | tipo_documento  | contestacion       |
      | procedimiento   | ordinario          |
      | dias_plazo      | 15                 |
      | tipo_dia        | habil              |
      | fecha_inicio    | 2025-01-15         |
      | rol             | 123456789          |
      | rut_cliente     | 12345678-9         |
      | clave_cliente   | cliente123         |
      | estado          | corriendo          |
    Entonces debería ser redirigido a "el calendario"
    Y debería haber 1 plazos en el sistema

  Escenario: Abogado puede crear un plazo de demanda
    Dado que estoy autenticado como "abogado"
    Y que estoy en la página de inicio
    Cuando hago clic en "el botón de crear plazo"
    Y lleno el formulario de "crear plazo" con
      | campo           | valor              |
      | tipo_documento  | demanda            |
      | procedimiento   | ordinario          |
      | dias_plazo      | 30                 |
      | tipo_dia        | habil              |
      | fecha_inicio    | 2025-01-20         |
      | rol             | 987654321          |
      | rut_cliente     | 87654321-0         |
      | clave_cliente   | cliente456         |
      | estado          | corriendo          |
    Entonces debería ser redirigido a "el calendario"
    Y debería haber 1 plazos en el sistema

  Escenario: Abogado puede crear un plazo de días corridos
    Dado que estoy autenticado como "abogado"
    Y que estoy en la página de inicio
    Cuando hago clic en "el botón de crear plazo"
    Y lleno el formulario de "crear plazo" con
      | campo           | valor              |
      | tipo_documento  | recurso            |
      | procedimiento   | sumario            |
      | dias_plazo      | 5                  |
      | tipo_dia        | corrido            |
      | fecha_inicio    | 2025-01-25         |
      | rol             | 555666777          |
      | rut_cliente     | 11223344-5         |
      | clave_cliente   | cliente789         |
      | estado          | corriendo          |
    Entonces debería ser redirigido a "el calendario"
    Y debería haber 1 plazos en el sistema

  Escenario: Abogado puede ver sus plazos en el calendario
    Dado que estoy autenticado como "abogado"
    Y que tengo un plazo judicial creado
    Cuando hago clic en "el botón de calendario"
    Entonces debería ver "el calendario"
    Y debería ver "el plazo en la lista"

  Escenario: Abogado puede ver detalles de un plazo
    Dado que estoy autenticado como "abogado"
    Y que tengo un plazo judicial creado
    Cuando hago clic en "el plazo en la lista"
    Entonces debería ver "los detalles del plazo"
    Y debería ver "la información del cliente"
    Y debería ver "la fecha de vencimiento"

  Escenario: Abogado puede buscar plazos por RUT del cliente
    Dado que estoy autenticado como "abogado"
    Y que tengo un plazo judicial creado
    Cuando busco por "rut_cliente" con valor "12345678-9"
    Entonces debería ver "el plazo en la lista"

  Escenario: Abogado puede buscar plazos por rol
    Dado que estoy autenticado como "abogado"
    Y que tengo un plazo judicial creado
    Cuando busco por "rol" con valor "123456789"
    Entonces debería ver "el plazo en la lista"

  Escenario: Abogado puede buscar plazos por tipo de documento
    Dado que estoy autenticado como "abogado"
    Y que tengo un plazo judicial creado
    Cuando busco por "tipo_documento" con valor "contestacion"
    Entonces debería ver "el plazo en la lista"

  Escenario: Abogado puede buscar plazos por estado
    Dado que estoy autenticado como "abogado"
    Y que tengo un plazo judicial creado
    Cuando busco por "estado" con valor "corriendo"
    Entonces debería ver "el plazo en la lista"

  Escenario: Sistema calcula automáticamente la fecha de vencimiento para días hábiles
    Dado que estoy autenticado como "abogado"
    Y que tengo un plazo judicial creado
    Entonces el plazo debería tener estado "corriendo"
    Y la fecha de vencimiento debería ser calculada correctamente
    Y la fecha de vencimiento debería excluir fines de semana y feriados

  Escenario: Sistema calcula automáticamente la fecha de vencimiento para días corridos
    Dado que estoy autenticado como "abogado"
    Y que creo un plazo con días corridos
    Entonces la fecha de vencimiento debería incluir todos los días
    Y la fecha de vencimiento debería ser calculada correctamente

  Escenario: Abogado puede editar un plazo existente
    Dado que estoy autenticado como "abogado"
    Y que tengo un plazo judicial creado
    Cuando hago clic en "el botón de editar plazo"
    Y modifico el campo "dias_plazo" con valor "20"
    Entonces el plazo debería ser actualizado
    Y la fecha de vencimiento debería ser recalculada

  Escenario: Abogado puede cambiar el estado de un plazo
    Dado que estoy autenticado como "abogado"
    Y que tengo un plazo judicial creado
    Cuando cambio el estado del plazo a "suspendido"
    Entonces el plazo debería tener estado "suspendido"

  Escenario: Abogado puede agregar observaciones a un plazo
    Dado que estoy autenticado como "abogado"
    Y que tengo un plazo judicial creado
    Cuando hago clic en "el botón de editar plazo"
    Y agrego observaciones "Reunión con cliente programada"
    Entonces las observaciones deberían ser guardadas

  Escenario: Abogado puede adjuntar un documento a un plazo
    Dado que estoy autenticado como "abogado"
    Y que tengo un plazo judicial creado
    Cuando hago clic en "el botón de editar plazo"
    Y adjunto un documento "contrato.pdf"
    Entonces el documento debería ser guardado
    Y debería poder ver el documento adjunto

  Escenario: Abogado puede eliminar un plazo
    Dado que estoy autenticado como "abogado"
    Y que tengo un plazo judicial creado
    Cuando hago clic en "el botón de eliminar plazo"
    Y confirmo la eliminación
    Entonces el plazo debería ser eliminado
    Y no debería ver "el plazo en la lista"

  Escenario: Abogado puede ver plazos vencidos
    Dado que estoy autenticado como "abogado"
    Y que tengo un plazo vencido
    Cuando hago clic en "el botón de calendario"
    Entonces debería ver "plazos vencidos"
    Y el plazo vencido debería estar marcado como "vencido"

  Escenario: Abogado puede ver plazos próximos a vencer
    Dado que estoy autenticado como "abogado"
    Y que tengo un plazo próximo a vencer
    Cuando hago clic en "el botón de calendario"
    Entonces debería ver "plazos próximos a vencer"
    Y el plazo debería estar marcado como "urgente"

  Escenario: Abogado puede filtrar plazos por fecha
    Dado que estoy autenticado como "abogado"
    Y que tengo varios plazos creados
    Cuando filtro por fecha desde "2025-01-01" hasta "2025-01-31"
    Entonces debería ver solo los plazos del mes de enero

  Escenario: Abogado puede ordenar plazos por fecha de vencimiento
    Dado que estoy autenticado como "abogado"
    Y que tengo varios plazos creados
    Cuando ordeno por "fecha de vencimiento"
    Entonces los plazos deberían estar ordenados cronológicamente

  Escenario: Abogado puede ver estadísticas de plazos
    Dado que estoy autenticado como "abogado"
    Y que tengo varios plazos creados
    Cuando hago clic en "el botón de estadísticas"
    Entonces debería ver "el total de plazos"
    Y debería ver "plazos vencidos"
    Y debería ver "plazos corriendo"
    Y debería ver "plazos suspendidos"

  Escenario: Abogado puede buscar plazos por RUT específico
    Dado que estoy autenticado como "abogado"
    Y que tengo plazos de diferentes clientes
    Cuando busco plazos por RUT "12345678-9"
    Entonces debería ver la lista de plazos
    Y debería ver "1" plazos en la lista

  Escenario: Abogado puede buscar plazos por rol específico
    Dado que estoy autenticado como "abogado"
    Y que tengo un plazo judicial creado
    Cuando busco plazos por rol "R-001-2025"
    Entonces debería ver la lista de plazos

  Escenario: Abogado puede filtrar plazos por tipo de documento
    Dado que estoy autenticado como "abogado"
    Y que tengo un plazo de contestación
    Y que tengo un plazo de demanda
    Cuando filtro por tipo de documento "demanda"
    Entonces debería ver la lista de plazos
    Y debería ver plazos ordenados por "fecha_vencimiento"

  Escenario: Abogado puede filtrar plazos por estado
    Dado que estoy autenticado como "abogado"
    Y que tengo plazos vencidos
    Cuando filtro por estado "vencido"
    Entonces debería ver la lista de plazos
    Y los plazos vencidos deberían estar marcados claramente

  Escenario: Abogado puede filtrar plazos por rango de fechas
    Dado que estoy autenticado como "abogado"
    Y que tengo varios plazos creados
    Cuando filtro por rango de fechas desde "2025-01-01" hasta "2025-12-31"
    Entonces debería ver la lista de plazos

  Escenario: Abogado puede ordenar plazos por diferentes campos
    Dado que estoy autenticado como "abogado"
    Y que tengo varios plazos creados
    Cuando ordeno por "fecha_vencimiento"
    Entonces debería ver plazos ordenados por "fecha_vencimiento"
    Y los plazos deberían estar ordenados por fecha de vencimiento

  Escenario: Abogado puede ver formulario de creación de plazo
    Dado que estoy autenticado como "abogado"
    Cuando hago clic en "crear plazo"
    Entonces debería ver el formulario de creación de plazo

  Escenario: Abogado puede ver formulario de edición de plazo
    Dado que estoy autenticado como "abogado"
    Y que tengo un plazo judicial creado
    Cuando hago clic en "editar plazo"
    Entonces debería ver el formulario de edición de plazo

  Escenario: Abogado puede ver filtros de búsqueda
    Dado que estoy autenticado como "abogado"
    Cuando accedo al calendario
    Entonces debería ver los filtros de búsqueda

  Escenario: Abogado puede agregar observaciones a un plazo
    Dado que estoy autenticado como "abogado"
    Y que tengo un plazo judicial creado
    Cuando edito el plazo con observaciones "Plazo importante para el cliente"
    Entonces el plazo debería tener observaciones

  Escenario: Abogado puede adjuntar documento a un plazo
    Dado que estoy autenticado como "abogado"
    Y que tengo un plazo judicial creado
    Cuando adjunto un documento al plazo
    Entonces el plazo debería tener documento adjunto

  Escenario: Sistema calcula fecha de vencimiento específica para días hábiles
    Dado que estoy autenticado como "abogado"
    Y que tengo un plazo de contestación
    Cuando verifico la fecha de vencimiento
    Entonces la fecha de vencimiento debería ser calculada correctamente

  Escenario: Sistema calcula fecha de vencimiento específica para días corridos
    Dado que estoy autenticado como "abogado"
    Y que tengo un plazo de días corridos
    Cuando verifico la fecha de vencimiento
    Entonces la fecha de vencimiento debería ser calculada correctamente

  Escenario: Abogado puede cambiar estado de plazo a suspendido
    Dado que estoy autenticado como "abogado"
    Y que tengo un plazo judicial creado
    Cuando cambio el estado del plazo a "suspendido"
    Entonces el plazo debería estar en estado "suspendido"

  Escenario: Abogado puede cambiar estado de plazo a vencido
    Dado que estoy autenticado como "abogado"
    Y que tengo un plazo judicial creado
    Cuando cambio el estado del plazo a "vencido"
    Entonces el plazo debería estar en estado "vencido"

  Escenario: Abogado puede crear plazo con código de procedimiento civil
    Dado que estoy autenticado como "abogado"
    Y que estoy en la página de inicio
    Cuando hago clic en "el botón de crear plazo"
    Y lleno el formulario de "crear plazo" con
      | campo           | valor              |
      | tipo_documento  | demanda            |
      | procedimiento   | Art. 254 CPC       |
      | fecha_inicio    | 2025-01-15         |
      | rol             | 987654321          |
      | rut_cliente     | 12345678-9         |
      | clave_cliente   | cliente_test       |
      | observaciones   | Demanda por daños   |
    Entonces debería ser redirigido a "el calendario"
    Y debería ver "el mensaje de confirmación"

  Escenario: Abogado puede crear plazo de días corridos
    Dado que estoy autenticado como "abogado"
    Y que estoy en la página de inicio
    Cuando hago clic en "el botón de crear plazo"
    Y lleno el formulario de "crear plazo" con
      | campo           | valor              |
      | tipo_documento  | sentencia          |
      | procedimiento   | ejecutivo          |
      | dias_plazo      | 30                 |
      | tipo_dia        | corrido            |
      | fecha_inicio    | 2025-01-15         |
      | rol             | 555666777          |
      | rut_cliente     | 98765432-1         |
      | clave_cliente   | cliente_sentencia  |
      | observaciones   | Sentencia ejecutiva |
    Entonces debería ser redirigido a "el calendario"
    Y debería ver "el mensaje de confirmación"

  Escenario: Abogado puede crear plazo con documento adjunto
    Dado que estoy autenticado como "abogado"
    Y que estoy en la página de inicio
    Cuando hago clic en "el botón de crear plazo"
    Y lleno el formulario de "crear plazo" con
      | campo           | valor              |
      | tipo_documento  | recurso            |
      | procedimiento   | apelacion          |
      | dias_plazo      | 10                 |
      | tipo_dia        | habil              |
      | fecha_inicio    | 2025-01-15         |
      | rol             | 111222333          |
      | rut_cliente     | 11223344-5         |
      | clave_cliente   | cliente_recurso    |
      | observaciones   | Recurso de apelación |
    Y adjunto un documento al plazo
    Entonces debería ser redirigido a "el calendario"
    Y debería ver "el mensaje de confirmación"

  Escenario: Abogado puede buscar plazos por RUT de cliente
    Dado que estoy autenticado como "abogado"
    Y que tengo plazos de diferentes clientes
    Cuando hago clic en "el botón de calendario"
    Y busco por "RUT de cliente" con valor "12345678-9"
    Entonces debería ver "solo plazos del cliente seleccionado"

  Escenario: Abogado puede filtrar plazos por estado vencido
    Dado que estoy autenticado como "abogado"
    Y que tengo plazos vencidos
    Cuando hago clic en "el botón de calendario"
    Y filtro por "estado" con valor "vencido"
    Entonces debería ver "plazos vencidos"

  Escenario: Abogado puede ordenar plazos por fecha de vencimiento
    Dado que estoy autenticado como "abogado"
    Y que tengo varios plazos creados
    Cuando hago clic en "el botón de calendario"
    Y ordeno por "fecha de vencimiento"
    Entonces debería ver "plazos ordenados cronológicamente"

  Escenario: Abogado puede ver plazos próximos a vencer
    Dado que estoy autenticado como "abogado"
    Y que tengo plazos próximos a vencer
    Cuando hago clic en "el botón de calendario"
    Y filtro por "estado" con valor "corriendo"
    Entonces debería ver "plazos próximos a vencer"

  Escenario: Abogado puede editar observaciones de un plazo
    Dado que estoy autenticado como "abogado"
    Y que tengo un plazo de contestación
    Cuando hago clic en "el botón de editar plazo"
    Y edito el plazo con observaciones "Observaciones actualizadas"
    Entonces debería ver "el mensaje de confirmación"
    Y el plazo debería tener observaciones

  Escenario: Abogado puede cambiar estado de plazo a suspendido
    Dado que estoy autenticado como "abogado"
    Y que tengo un plazo de contestación
    Cuando hago clic en "el botón de editar plazo"
    Y cambio el estado del plazo a "suspendido"
    Entonces debería ver "el mensaje de confirmación"
    Y el plazo debería estar en estado "suspendido"

  Escenario: Abogado puede ver detalles completos de un plazo
    Dado que estoy autenticado como "abogado"
    Y que tengo un plazo de contestación
    Cuando hago clic en "el plazo en la lista"
    Entonces debería ver "los detalles del plazo"
    Y debería ver "la información del cliente"
    Y debería ver "la fecha de vencimiento"

  Escenario: Abogado puede eliminar un plazo
    Dado que estoy autenticado como "abogado"
    Y que tengo un plazo de contestación
    Cuando hago clic en "el botón de eliminar plazo"
    Entonces debería ver "el mensaje de confirmación"

  Escenario: Abogado puede crear plazo con validación de RUT
    Dado que estoy autenticado como "abogado"
    Y que estoy en la página de inicio
    Cuando hago clic en "el botón de crear plazo"
    Y lleno el formulario de "crear plazo" con
      | campo           | valor              |
      | tipo_documento  | demanda            |
      | procedimiento   | ordinario          |
      | dias_plazo      | 20                 |
      | tipo_dia        | habil              |
      | fecha_inicio    | 2025-01-15         |
      | rol             | 999888777          |
      | rut_cliente     | 12345678-9         |
      | clave_cliente   | cliente_valido     |
      | observaciones   | Plazo con RUT válido |
    Entonces debería ser redirigido a "el calendario"
    Y debería ver "el mensaje de confirmación"

  Escenario: Abogado puede crear plazo con fecha de inicio futura
    Dado que estoy autenticado como "abogado"
    Y que estoy en la página de inicio
    Cuando hago clic en "el botón de crear plazo"
    Y lleno el formulario de "crear plazo" con
      | campo           | valor              |
      | tipo_documento  | contestacion       |
      | procedimiento   | ordinario          |
      | dias_plazo      | 15                 |
      | tipo_dia        | habil              |
      | fecha_inicio    | 2025-02-01         |
      | rol             | 444555666          |
      | rut_cliente     | 22334455-6         |
      | clave_cliente   | cliente_futuro     |
      | observaciones   | Plazo futuro       |
    Entonces debería ser redirigido a "el calendario"
    Y debería ver "el mensaje de confirmación"
