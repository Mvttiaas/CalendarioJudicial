# language: es
# encoding: utf-8

Característica: Gestión de perfil de usuario
  Como usuario del sistema
  Quiero poder gestionar mi perfil personal
  Para mantener actualizada mi información

  Escenario: Usuario puede acceder a su perfil
    Dado que estoy autenticado como "abogado"
    Cuando hago clic en "mi perfil"
    Entonces debería ver "la página de perfil"
    Y debería ver "mi información personal"

  Escenario: Usuario puede ver su información personal
    Dado que estoy autenticado como "abogado"
    Y que hago clic en "mi perfil"
    Entonces debería ver "mi nombre completo"
    Y debería ver "mi email"
    Y debería ver "mi RUT"
    Y debería ver "mi tipo de usuario"
    Y debería ver "mi número de licencia"

  Escenario: Usuario puede actualizar su información personal
    Dado que estoy autenticado como "abogado"
    Y que hago clic en "mi perfil"
    Cuando modifico mi información con
      | campo      | valor_nuevo        |
      | first_name | Juan Carlos        |
      | last_name  | Pérez González     |
      | email      | juan@nuevo.com     |
    Entonces la información debería ser actualizada
    Y debería ver "Perfil actualizado exitosamente"

  Escenario: Usuario puede cambiar su contraseña
    Dado que estoy autenticado como "abogado"
    Y que hago clic en "mi perfil"
    Cuando hago clic en "cambiar contraseña"
    Y lleno el formulario de cambio de contraseña con
      | campo              | valor        |
      | password_actual    | testpass123  |
      | password_nueva     | newpass456   |
      | password_confirmar | newpass456   |
    Entonces la contraseña debería ser cambiada
    Y debería ver "Contraseña actualizada exitosamente"

  Escenario: Usuario no puede cambiar contraseña con contraseña actual incorrecta
    Dado que estoy autenticado como "abogado"
    Y que hago clic en "mi perfil"
    Cuando hago clic en "cambiar contraseña"
    Y lleno el formulario de cambio de contraseña con
      | campo              | valor        |
      | password_actual    | password_incorrecta |
      | password_nueva     | newpass456   |
      | password_confirmar | newpass456   |
    Entonces debería ver "Contraseña actual incorrecta"

  Escenario: Usuario no puede cambiar contraseña con contraseñas nuevas diferentes
    Dado que estoy autenticado como "abogado"
    Y que hago clic en "mi perfil"
    Cuando hago clic en "cambiar contraseña"
    Y lleno el formulario de cambio de contraseña con
      | campo              | valor        |
      | password_actual    | testpass123  |
      | password_nueva     | newpass456   |
      | password_confirmar | differentpass |
    Entonces debería ver "Las contraseñas nuevas no coinciden"

  Escenario: Usuario puede cambiar su tema preferido
    Dado que estoy autenticado como "abogado"
    Y que hago clic en "mi perfil"
    Cuando cambio el tema a "oscuro"
    Entonces el tema debería cambiar a oscuro
    Y la interfaz debería verse con tema oscuro

  Escenario: Usuario puede cambiar el idioma
    Dado que estoy autenticado como "abogado"
    Y que hago clic en "mi perfil"
    Cuando cambio el idioma a "inglés"
    Entonces la interfaz debería cambiar a inglés
    Y los textos deberían estar en inglés

  Escenario: Usuario puede configurar plazos por página
    Dado que estoy autenticado como "abogado"
    Y que hago clic en "mi perfil"
    Cuando cambio "plazos por página" a "50"
    Entonces la configuración debería ser guardada
    Y el calendario debería mostrar 50 plazos por página

  Escenario: Usuario puede ver su historial de actividad
    Dado que estoy autenticado como "abogado"
    Y que hago clic en "mi perfil"
    Cuando hago clic en "historial de actividad"
    Entonces debería ver "mis acciones recientes"
    Y debería ver "fechas y horas de las acciones"

  Escenario: Usuario puede exportar sus datos
    Dado que estoy autenticado como "abogado"
    Y que hago clic en "mi perfil"
    Cuando hago clic en "exportar mis datos"
    Entonces debería recibir un archivo con "todos mis datos"
    Y el archivo debería contener "mi información personal"
    Y el archivo debería contener "mis plazos judiciales"

  Escenario: Usuario puede actualizar su información de contacto
    Dado que estoy autenticado como "abogado"
    Y que hago clic en "mi perfil"
    Cuando lleno el formulario de "perfil" con
      | campo      | valor                    |
      | first_name | Juan Carlos              |
      | last_name  | Pérez González           |
      | email      | juan.perez@abogado.cl    |
    Entonces debería ver "el mensaje de confirmación"
    Y la información debería ser actualizada

  Escenario: Usuario puede cambiar su contraseña con validación
    Dado que estoy autenticado como "abogado"
    Y que hago clic en "cambiar contraseña"
    Cuando lleno el formulario de "cambio de contraseña" con
      | campo              | valor           |
      | old_password       | testpass123     |
      | new_password1      | nueva_pass_456  |
      | new_password2      | nueva_pass_456  |
    Entonces debería ver "el mensaje de confirmación"
    Y la contraseña debería ser actualizada

  Escenario: Usuario no puede cambiar contraseña con datos incorrectos
    Dado que estoy autenticado como "abogado"
    Y que hago clic en "cambiar contraseña"
    Cuando lleno el formulario de "cambio de contraseña" con
      | campo              | valor           |
      | old_password       | password_falso  |
      | new_password1      | nueva_pass_456  |
      | new_password2      | nueva_pass_456  |
    Entonces debería ver "el mensaje de error específico"

  Escenario: Usuario puede configurar sus preferencias de tema
    Dado que estoy autenticado como "abogado"
    Y que hago clic en "mi perfil"
    Cuando cambio el tema a "oscuro"
    Entonces la configuración debería ser guardada
    Y el tema debería cambiar a oscuro

  Escenario: Usuario puede configurar idioma del sistema
    Dado que estoy autenticado como "abogado"
    Y que hago clic en "mi perfil"
    Cuando cambio el idioma a "español"
    Entonces la configuración debería ser guardada
    Y el idioma debería cambiar a español

  Escenario: Usuario puede ver su historial de actividad
    Dado que estoy autenticado como "abogado"
    Y que tengo actividad reciente
    Cuando hago clic en "historial de actividad"
    Entonces debería ver "mi historial de actividad"
    Y debería ver "las acciones recientes"

  Escenario: Usuario puede configurar notificaciones
    Dado que estoy autenticado como "abogado"
    Y que hago clic en "mi perfil"
    Cuando configuro las notificaciones
    Entonces la configuración debería ser guardada
    Y las notificaciones deberían estar activadas

  Escenario: Usuario puede ver estadísticas de su perfil
    Dado que estoy autenticado como "abogado"
    Y que tengo varios plazos creados
    Cuando hago clic en "mi perfil"
    Entonces debería ver "estadísticas de mi perfil"
    Y debería ver "el total de plazos creados"
    Y debería ver "plazos activos"

  Escenario: Usuario puede actualizar su información profesional
    Dado que estoy autenticado como "abogado"
    Y que hago clic en "mi perfil"
    Cuando actualizo mi información profesional
    Entonces debería ver "el mensaje de confirmación"
    Y la información profesional debería ser actualizada
