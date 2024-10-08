# Generated by Django 4.2.2 on 2024-07-29 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dmd_gui', '0002_rename_friend_newdata'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeatherData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
                ('spot', models.CharField(max_length=100)),
                ('plot_1', models.FloatField()),
                ('plot_2', models.FloatField()),
                ('plot_3', models.FloatField()),
                ('plot_4', models.FloatField()),
                ('plot_5', models.FloatField()),
                ('plot_6', models.FloatField()),
                ('plot_7', models.FloatField()),
                ('plot_8', models.FloatField()),
                ('plot_9', models.FloatField()),
                ('plot_10', models.FloatField()),
                ('plot_11', models.FloatField()),
                ('plot_12', models.FloatField()),
                ('plot_13', models.FloatField()),
                ('plot_14', models.FloatField()),
                ('plot_15', models.FloatField()),
                ('plot_16', models.FloatField()),
                ('plot_17', models.FloatField()),
                ('plot_18', models.FloatField()),
                ('plot_19', models.FloatField()),
                ('plot_20', models.FloatField()),
                ('plot_21', models.FloatField()),
                ('plot_22', models.FloatField()),
                ('plot_23', models.FloatField()),
                ('plot_24', models.FloatField()),
                ('index_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.DeleteModel(
            name='NewData',
        ),
    ]
