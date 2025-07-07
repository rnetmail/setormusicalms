# backend/api/serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import RepertorioItem, AgendaItem, RecadoItem, HistoriaItem, GaleriaItem

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class RepertorioItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepertorioItem
        fields = '__all__'

class AgendaItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgendaItem
        fields = '__all__'

class RecadoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecadoItem
        fields = '__all__'

class HistoriaItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoriaItem
        fields = '__all__'

class GaleriaItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = GaleriaItem
        fields = '__all__'
