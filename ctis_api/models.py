from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Pessoa(models.Model):
    class TipoPessoa(models.IntegerChoices):
        GESTOR = 1
        PROFESSOR = 2
        ALUNO = 3

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo_pessoa = models.IntegerField(choices=TipoPessoa.choices)
    nome = models.CharField(max_length = 30)
    cpf = models.CharField(max_length = 15)
    telefone = models.CharField(max_length = 20)
    data_vencimento = models.IntegerField()
    status = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        db_table  = 'pessoas'


class AlunoPagameto(models.Model):
    class Status(models.IntegerChoices):
        NAO_INICIADO = 1
        PAGAMENTO_GERADO = 2
        PAGAMETO_PENDENTE = 3
        PAGAMENTO_EFETUADO = 4

    pessoa_aluno = models.ForeignKey(Pessoa, on_delete=models.CASCADE)

    mes_referencia = models.IntegerField()
    valor = models.FloatField()
    link = models.CharField(max_length=200)
    status = models.IntegerField(choices=Status.choices, default=Status.NAO_INICIADO)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        db_table  = 'aluno_pagamentos'
