# backend/backend/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Qualquer URL que comece com 'api/' será enviada para o ficheiro de URLs da nossa app 'api'
    path('api/', include('api.urls')),
]
