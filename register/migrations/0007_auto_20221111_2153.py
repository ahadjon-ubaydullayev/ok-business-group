# Generated by Django 3.0 on 2022-11-12 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0006_auto_20221110_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='filled_date',
            field=models.CharField(max_length=255),
        ),
    ]
