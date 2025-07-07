# backend/api/views.py

from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from .models import RepertorioItem, AgendaItem, RecadoItem, HistoriaItem, GaleriaItem
from .serializers import (
    UserSerializer,
    RepertorioItemSerializer,
    AgendaItemSerializer,
    RecadoItemSerializer,
    HistoriaItemSerializer,
    GaleriaItemSerializer
)

# ViewSets para o Admin (CRUD completo)
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class RepertorioViewSet(viewsets.ModelViewSet):
    queryset = RepertorioItem.objects.all().order_by('-year', 'title')
    serializer_class = RepertorioItemSerializer
    permission_classes = [IsAdminOrReadOnly]

class AgendaViewSet(viewsets.ModelViewSet):
    queryset = AgendaItem.objects.all().order_by('-date')
    serializer_class = AgendaItemSerializer
    permission_classes = [IsAdminOrReadOnly]

class RecadoViewSet(viewsets.ModelViewSet):
    queryset = RecadoItem.objects.all().order_by('-date')
    serializer_class = RecadoItemSerializer
    permission_classes = [IsAdminOrReadOnly]

class HistoriaViewSet(viewsets.ModelViewSet):
    queryset = HistoriaItem.objects.all().order_by('year')
    serializer_class = HistoriaItemSerializer
    permission_classes = [IsAdminOrReadOnly]

class GaleriaViewSet(viewsets.ModelViewSet):
    queryset = GaleriaItem.objects.all().order_by('-id')
    serializer_class = GaleriaItemSerializer
    permission_classes = [IsAdminOrReadOnly]
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

# Views para Login e Logout
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    return Response({'error': 'Credenciais Inválidas'}, status=400)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    request.user.auth_token.delete()
    return Response(status=204)
