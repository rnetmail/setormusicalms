urlpatterns = [
    path('admin/', admin.site.urls),
    # CORRETO: Envia tudo que for /api/ para o ficheiro da app 'api'
    path('api/', include('api.urls')),
]
