# Generated by Django 4.2.2 on 2024-07-31 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dmd_gui', '0007_rename_demanddata1_demanddata0'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='demanddata0',
            name='prediction',
        ),
        migrations.AddField(
            model_name='demanddata0',
            name='prediction_n',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='demanddata0',
            name='prediction_q',
            field=models.FloatField(default=0.0),
        ),
    ]
