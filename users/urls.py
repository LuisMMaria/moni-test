from django.urls import path
from django.contrib.auth.decorators import login_required

# Import Views
from .views import CreateUser, ListUser, DeleteUser, UpdateUser

urlpatterns = [
    path('registrar_usuario/',
         login_required(CreateUser.as_view()), name='create_user'),
    path('lista_usuarios/',
         login_required(ListUser.as_view()), name='list_user'),
    path('eliminar_usuario/<int:pk>',
         login_required(DeleteUser.as_view()), name='delete_user'),
    path('editar_usuario/<int:pk>',
         login_required(UpdateUser.as_view()), name='edit_user'),
]
