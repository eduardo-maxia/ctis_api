# Generated by Django 4.1.3 on 2022-11-17 00:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ctis_api', '0003_rename_alunopagametos_alunopagameto_and_more'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='alunopagameto',
            table='aluno_pagamentos',
        ),
        migrations.AlterModelTable(
            name='pessoa',
            table='pessoas',
        ),
    ]
