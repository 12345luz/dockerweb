# Generated by Django 5.1.1 on 2024-11-05 20:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appips', '0006_alter_usuario_codigo_ocupacion'),
    ]

    operations = [
        migrations.CreateModel(
            name='Medico',
            fields=[
                ('numero_identificacion', models.CharField(max_length=18, primary_key=True, serialize=False)),
                ('tipo_identificacion', models.CharField(choices=[('CE', 'Cédula De Extranjería'), ('CC', 'Cédula De Ciudadanía'), ('PA', 'Pasaporte'), ('CD', 'Carnet Diplomático')], max_length=2)),
                ('primer_apellido', models.CharField(max_length=30)),
                ('segundo_apellido', models.CharField(max_length=30)),
                ('primer_nombre', models.CharField(max_length=30)),
                ('segundo_nombre', models.CharField(max_length=30)),
                ('especialidad_medica', models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='citas',
            name='medico',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='citas', to='appips.medico'),
        ),
        migrations.DeleteModel(
            name='Medicos',
        ),
    ]
