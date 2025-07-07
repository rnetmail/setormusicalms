# backend/backend/urls.py

from django.contrib import admin
# A linha abaixo importa as funções 'path' e 'include'
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
