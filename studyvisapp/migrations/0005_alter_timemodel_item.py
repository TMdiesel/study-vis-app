# Generated by Django 3.2.6 on 2021-08-12 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studyvisapp', '0004_auto_20210812_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timemodel',
            name='item',
            field=models.CharField(choices=[('danger', '機械学習'), ('warning', '統計'), ('primary', '読書')], max_length=50),
        ),
    ]
