# backend/api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter

# IMPORTANTE: Importe aqui as suas classes de Views do ficheiro views.py
# O nome 'views' pode ser diferente se você organizou de outra forma.
from . import views

# O router cria automaticamente as URLs para os seus ViewSets (ex: /repertorio/ e /repertorio/1/)
router = DefaultRouter()

# ATENÇÃO: Os nomes 'RepertorioViewSet', 'AgendaViewSet' etc. devem ser
# exatamente os mesmos nomes das classes que você criou no seu ficheiro 'api/views.py'.
# Se os nomes forem diferentes, ajuste-os aqui.
router.register(r'repertorio', views.RepertorioViewSet, basename='repertorio')
router.register(r'agenda', views.AgendaViewSet, basename='agenda')
router.register(r'recados', views.RecadoViewSet, basename='recados')
router.register(r'users', views.UserViewSet, basename='user')


# O urlpatterns começa com as URLs geradas pelo router e adiciona as de login/logout
urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
