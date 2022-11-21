from django.contrib.auth.models import User
from django.db import models


class DemoModel(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    image = models.ImageField(upload_to="demo_images")

    def __str__(self):
        return self.title


# Create your models here.


class Pessoa(models.Model):
    class TipoPessoa(models.IntegerChoices):
        GESTOR = 1
        PROFESSOR = 2
        ALUNO_ADULTO = 3
        ALUNO_INFANTIL = 4

    class Status(models.IntegerChoices):
        ATIVO = 1
        INATIVO = 2

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo_pessoa = models.IntegerField(choices=TipoPessoa.choices)
    nome = models.CharField(max_length=30)
    nome_responsavel = models.CharField(max_length=30, blank=True)
    data_vencimento = models.IntegerField(choices=Status.choices, null=True)
    status = models.IntegerField(choices=Status.choices, default=Status.ATIVO)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        db_table = 'pessoas'


class Sede(models.Model):
    nome = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        db_table = 'sedes'


class Turma(models.Model):
    class TipoDias(models.IntegerChoices):
        SEGUNDA_QUARTA = 1
        TERCA_QUINTA = 2

    sede = models.ForeignKey(Sede, on_delete=models.CASCADE)
    tipo_dias = models.IntegerField(choices=TipoDias.choices)
    horario = models.CharField(max_length=10)
    pessoa_professor = models.ForeignKey(
        Pessoa, on_delete=models.SET_NULL, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        db_table = 'turmas'


class TurmaAluno(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    pessoa_aluno = models.ForeignKey(Pessoa, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        db_table = 'turma_alunos'


class Mes(models.Model):
    def mes_serialized(self):
        return self.Meses.names[self.mes]

    class Meses(models.IntegerChoices):
        Janeiro = 1
        Fevereiro = 2
        Marco = 3
        Abril = 4
        Maio = 5
        Junho = 6
        Julho = 7
        Agosto = 8
        Setembro = 9
        Outubro = 10
        Novembro = 11
        Dezembro = 12
    
    ano_letivo = models.IntegerField()
    mes = models.IntegerField(choices=Meses.choices)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        db_table = 'meses'


class TurmaAlunoPagamento(models.Model):
    class Status(models.IntegerChoices):
        PAGAMENTO_GERADO = 1
        PAGAMETO_PENDENTE = 2
        PAGAMENTO_EFETUADO = 3

    turma_aluno = models.ForeignKey(TurmaAluno, on_delete=models.CASCADE)

    mes_referencia = models.ForeignKey(Mes, on_delete=models.CASCADE)
    valor = models.FloatField()
    link = models.CharField(max_length=200, default='')
    status = models.IntegerField(
        choices=Status.choices, default=Status.PAGAMENTO_GERADO)
    data_pagamento = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        db_table = 'aluno_pagamentos'


class Configuracoes(models.Model):
    ano_letivo = models.IntegerField()
    last_transaction = models.CharField(max_length=1000)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        db_table = 'configuracoes'
