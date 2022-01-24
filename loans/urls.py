from django.urls import path
from django.contrib.auth.decorators import login_required

# Import Views
from .views import CreateLoan, ResultApproved, ListLoan, DeleteLoan

urlpatterns = [
    path('pedido_prestamo/', CreateLoan.as_view(), name='create_loan'),
    path('resultado_prestamo/', ResultApproved.as_view(), name='loan_result'),
    path(
        'lista_prestamos/',
        login_required(ListLoan.as_view()),
        name='list_loan'
        ),
    path(
        'eliminar_prestamo/<int:pk>',
        login_required(DeleteLoan.as_view()),
        name='delete_loan'
        ),
]
