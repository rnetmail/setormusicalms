# backend/api/views.py

from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

# Importa os modelos e serializers
from .models import (
    RepertorioItem, 
    AgendaItem, 
    RecadoItem, 
    HistoriaItem, 
    GaleriaItem
)
from .serializers import (
    UserSerializer,
    RepertorioItemSerializer,
    AgendaItemSerializer,
    RecadoItemSerializer,
    HistoriaItemSerializer,
    GaleriaItemSerializer
)

# --- Classes de Permissão Customizadas ---

class IsSuperAdminUser(permissions.BasePermission):
    """
    Permite acesso apenas a super-utilizadores (para o CRUD de utilizadores).
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Permite que qualquer um leia (GET), mas apenas membros da equipa (staff) podem escrever (POST, PUT, DELETE).
    """
    def has_permission(self, request, view):
        # Permite pedidos de leitura (GET, HEAD, OPTIONS) a qualquer um.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Permite pedidos de escrita apenas a utilizadores que sejam staff.
        return request.user and request.user.is_staff

# --- ViewSets para cada Modelo ---

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint para ver e editar utilizadores.
    Apenas Super Admins podem aceder.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsSuperAdminUser]


class RepertorioViewSet(viewsets.ModelViewSet):
    """
    API endpoint para o Repertório.
    """
    queryset = RepertorioItem.objects.all().order_by('-year', 'title')
    serializer_class = RepertorioItemSerializer
    permission_classes = [IsStaffOrReadOnly] # Qualquer um pode ver, mas só staff pode editar.


class AgendaViewSet(viewsets.ModelViewSet):
    """
    API endpoint para a Agenda.
    """
    queryset = AgendaItem.objects.all().order_by('-date')
    serializer_class = AgendaItemSerializer
    permission_classes = [IsStaffOrReadOnly]


class RecadoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para os Recados.
    """
    queryset = RecadoItem.objects.all().order_by('-date')
    serializer_class = RecadoItemSerializer
    permission_classes = [IsStaffOrReadOnly]


class HistoriaViewSet(viewsets.ModelViewSet):
    """
    API endpoint para a História.
    """
    queryset = HistoriaItem.objects.all().order_by('year')
    serializer_class = HistoriaItemSerializer
    permission_classes = [IsStaffOrReadOnly]


class GaleriaViewSet(viewsets.ModelViewSet):
    """
    API endpoint para a Galeria.
    """
    queryset = GaleriaItem.objects.all().order_by('-id')
    serializer_class = GaleriaItemSerializer
    permission_classes = [IsStaffOrReadOnly]


# --- Views Customizadas para Login/Logout ---

@api_view(['POST'])
@permission_classes([permissions.AllowAny]) # Qualquer um pode tentar fazer login
def login_view(request):
    """
    Recebe 'username' e 'password' e retorna um token de autenticação.
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    
    if user:
        # Se o utilizador for autenticado com sucesso, obtém ou cria um token para ele
        token, _ = Token.objects.get_or_create(user=user)
        # Retorna os dados do utilizador juntamente com o token
        serializer = UserSerializer(user)
        return Response({
            'token': token.key,
            'user': serializer.data
        })
        
    return Response({'error': 'Credenciais Inválidas'}, status=400)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated]) # Apenas utilizadores autenticados podem fazer logout
def logout_view(request):
    """
    Apaga o token de autenticação do utilizador, invalidando a sua sessão.
    """
    try:
        # Apaga o token associado ao utilizador que fez o pedido
        request.user.auth_token.delete()
        return Response({'status': 'logout bem-sucedido'}, status=200)
    except (AttributeError, Token.DoesNotExist):
        return Response({'error': 'Nenhum token encontrado para o utilizador.'}, status=400)
