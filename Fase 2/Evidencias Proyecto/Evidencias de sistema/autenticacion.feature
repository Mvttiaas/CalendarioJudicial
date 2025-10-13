# language: es
# encoding: utf-8

Característica: Autenticación de usuarios
  Como usuario del sistema
  Quiero poder iniciar sesión y registrarme
  Para acceder a las funcionalidades del calendario judicial

  Escenario: Usuario puede acceder a la página de login
    Dado que estoy en la página de inicio
    Cuando hago clic en "el botón de login"
    Entonces debería ver "el formulario de login"

  Escenario: Usuario puede acceder a la página de registro
    Dado que estoy en la página de inicio
    Cuando hago clic en "el botón de registro"
    Entonces debería ver "el formulario de registro"

  Escenario: Usuario puede registrarse como abogado
    Dado que estoy en la página de inicio
    Cuando hago clic en "el botón de registro"
    Y lleno el formulario de "registro" con
      | campo           | valor              |
      | username        | test_abogado       |
      | email           | test@example.com   |
      | password1       | testpass123        |
      | password2       | testpass123        |
      | tipo_usuario    | abogado            |
      | numero_licencia | 1234567-8          |
      | rut             | 12345678-9         |
      | first_name      | Test               |
      | last_name       | User               |
    Entonces debería ser redirigido a "el dashboard"

  Escenario: Usuario puede registrarse como juez
    Dado que estoy en la página de inicio
    Cuando hago clic en "el botón de registro"
    Y lleno el formulario de "registro" con
      | campo           | valor              |
      | username        | test_juez          |
      | email           | juez@example.com   |
      | password1       | testpass123        |
      | password2       | testpass123        |
      | tipo_usuario    | juez               |
      | numero_licencia | JUEZ-12345         |
      | rut             | 87654321-0         |
      | first_name      | Juez               |
      | last_name       | Test               |
    Entonces debería ser redirigido a "el dashboard"

  Escenario: Usuario puede registrarse como asistente legal
    Dado que estoy en la página de inicio
    Cuando hago clic en "el botón de registro"
    Y lleno el formulario de "registro" con
      | campo           | valor              |
      | username        | test_asistente     |
      | email           | asistente@example.com |
      | password1       | testpass123        |
      | password2       | testpass123        |
      | tipo_usuario    | asistente          |
      | numero_licencia | LICENCIA123        |
      | rut             | 11223344-5         |
      | first_name      | Asistente          |
      | last_name       | Legal              |
    Entonces debería ser redirigido a "el dashboard"

  Escenario: Usuario puede iniciar sesión con username
    Dado que estoy autenticado como "abogado"
    Cuando hago clic en "el botón de login"
    Y lleno el formulario de "login" con
      | campo    | valor        |
      | username | test_abogado |
      | password | testpass123  |
    Entonces debería ser redirigido a "el dashboard"

  Escenario: Usuario puede iniciar sesión con email
    Dado que estoy autenticado como "abogado"
    Cuando hago clic en "el botón de login"
    Y lleno el formulario de "login" con
      | campo    | valor            |
      | username | test@example.com |
      | password | testpass123      |
    Entonces debería ser redirigido a "el dashboard"

  Escenario: Usuario no puede iniciar sesión con credenciales incorrectas
    Dado que estoy en la página de inicio
    Cuando hago clic en "el botón de login"
    Y lleno el formulario de "login" con
      | campo    | valor        |
      | username | usuario_falso|
      | password | password_falso|
    Entonces debería ver "Credenciales inválidas"

  Escenario: Usuario no puede registrarse con contraseñas diferentes
    Dado que estoy en la página de inicio
    Cuando hago clic en "el botón de registro"
    Y lleno el formulario de "registro" con
      | campo           | valor              |
      | username        | test_user          |
      | email           | test@example.com   |
      | password1       | testpass123        |
      | password2       | testpass456        |
      | tipo_usuario    | abogado            |
      | numero_licencia | 1234567-8          |
      | rut             | 12345678-9         |
      | first_name      | Test               |
      | last_name       | User               |
    Entonces debería ver "Las contraseñas no coinciden"

  Escenario: Usuario no puede registrarse con RUT inválido
    Dado que estoy en la página de inicio
    Cuando hago clic en "el botón de registro"
    Y lleno el formulario de "registro" con
      | campo           | valor              |
      | username        | test_user          |
      | email           | test@example.com   |
      | password1       | testpass123        |
      | password2       | testpass123        |
      | tipo_usuario    | abogado            |
      | numero_licencia | 1234567-8          |
      | rut             | 123456-7           |
      | first_name      | Test               |
      | last_name       | User               |
    Entonces debería ver "RUT inválido"

  Escenario: Usuario no puede registrarse con email inválido
    Dado que estoy en la página de inicio
    Cuando hago clic en "el botón de registro"
    Y lleno el formulario de "registro" con
      | campo           | valor              |
      | username        | test_user          |
      | email           | email_invalido     |
      | password1       | testpass123        |
      | password2       | testpass123        |
      | tipo_usuario    | abogado            |
      | numero_licencia | 1234567-8          |
      | rut             | 12345678-9         |
      | first_name      | Test               |
      | last_name       | User               |
    Entonces debería ver "Email inválido"

  Escenario: Usuario puede cerrar sesión
    Dado que estoy autenticado como "abogado"
    Cuando hago clic en "el botón de cerrar sesión"
    Entonces debería ser redirigido a "la página de inicio"
    Y debería ver "Sesión cerrada exitosamente"
