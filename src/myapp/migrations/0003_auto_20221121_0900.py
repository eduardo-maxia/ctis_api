# Generated by Django 3.1.8 on 2022-11-21 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_auto_20221120_1923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turmaalunopagamento',
            name='status',
            field=models.IntegerField(choices=[(1, 'Agendado'), (2, 'Proximo'), (3, 'Pendente'), (4, 'Aprovado')], default=1),
        ),
    ]