from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import TurmaAlunoPagamento, Pessoa, Turma, TurmaAluno


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class PessoaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pessoa
        fields = '__all__'

class TurmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turma
        fields = '__all__'

class TurmaAlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TurmaAluno
        fields = '__all__'

class TurmaAlunoPagamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TurmaAlunoPagamento
        fields = '__all__'
