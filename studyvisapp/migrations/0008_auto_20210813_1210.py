# Generated by Django 3.2.6 on 2021-08-13 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studyvisapp', '0007_auto_20210813_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timemodel',
            name='endtime',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='timemodel',
            name='starttime',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]
