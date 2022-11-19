# Generated by Django 3.1.8 on 2022-11-19 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_remove_pessoa_cpf'),
    ]

    operations = [
        migrations.AddField(
            model_name='pessoa',
            name='nome_responsavel',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='tipo_pessoa',
            field=models.IntegerField(choices=[(1, 'Gestor'), (2, 'Professor'), (3, 'Aluno Adulto'), (4, 'Aluno Infantil')]),
        ),
    ]
