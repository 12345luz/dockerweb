# Generated by Django 5.1.1 on 2024-10-29 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appips', '0002_medicos_citas_historiaclinica'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='codigo_pertenencia_etnica',
            field=models.SmallIntegerField(choices=[(1, 'Indígena'), (2, 'ROM (gitano)'), (3, 'Raizal (archipiélago de San Andrés y Providencia)'), (4, 'Palanquero de San Basilio'), (5, 'Negro(a), Mulato(a), Afrocolombiano(a) o Afro descendiente'), (6, 'Ninguna de las anteriores')]),
        ),
    ]