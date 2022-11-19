from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import TurmaAlunoPagamento, Pessoa


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class PessoaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pessoa
        fields = '__all__'

class TurmaAlunoPagamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TurmaAlunoPagamento
        fields = '__all__'
