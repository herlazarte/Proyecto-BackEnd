# Generated by Django 5.1 on 2024-11-16 18:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('solicitudes', '0002_initial'),
        ('turnos', '0001_initial'),
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='turno',
            name='profesional',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.profesional'),
        ),
        migrations.AddField(
            model_name='turno',
            name='solicitud',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='solicitudes.solicitud'),
        ),
    ]
