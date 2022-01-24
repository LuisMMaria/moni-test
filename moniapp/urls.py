from django.contrib import admin
from django.urls import path, include

from loans.views import Home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include(('users.api.urls', 'usersapi'))),
    path('loans/', include(('loans.api.urls', 'loansapi'))),
    path('', Home.as_view(), name='home'),
    path('usuarios/', include(('users.urls', 'users'))),
    path('prestamos/', include(('loans.urls', 'loans'))),
    path('accounts/', include('django.contrib.auth.urls')),
]
