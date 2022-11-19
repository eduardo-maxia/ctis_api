from django.db import models


class DemoModel(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    image = models.ImageField(upload_to="demo_images")

    def __str__(self):
        return self.title

from django.contrib.auth.models import User

# Create your models here.
class Pessoa(models.Model):
    class TipoPessoa(models.IntegerChoices):
        GESTOR = 1
        PROFESSOR = 2
        ALUNO_ADULTO = 3
        ALUNO_INFANTIL = 4

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo_pessoa = models.IntegerField(choices=TipoPessoa.choices)
    nome = models.CharField(max_length = 30)
    nome_responsavel = models.CharField(max_length = 30, blank=True)
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
        PAGAMENTO_GERADO = 1
        PAGAMETO_PENDENTE = 2
        PAGAMENTO_EFETUADO = 3

    pessoa_aluno = models.ForeignKey(Pessoa, on_delete=models.CASCADE)

    mes_referencia = models.IntegerField()
    valor = models.FloatField()
    link = models.CharField(max_length=200)
    status = models.IntegerField(choices=Status.choices, default=Status.PAGAMENTO_GERADO)
    data_pagamento = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        db_table  = 'aluno_pagamentos'


class Configuracoes(models.Model):
    ano_letivo = models.IntegerField()
    last_transaction = models.CharField(max_length=1000)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        db_table  = 'configuracoes'
