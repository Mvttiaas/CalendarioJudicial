from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil, name='perfil'),
    path('cambiar-password/', views.cambiar_password, name='cambiar_password'),
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('usuario/<int:usuario_id>/', views.detalle_usuario, name='detalle_usuario'),
    path('usuario/<int:usuario_id>/toggle/', views.toggle_usuario_activo, name='toggle_usuario_activo'),
    path('verificar-rut/', views.verificar_rut, name='verificar_rut'),
    path('verificar-email/', views.verificar_email, name='verificar_email'),
]

