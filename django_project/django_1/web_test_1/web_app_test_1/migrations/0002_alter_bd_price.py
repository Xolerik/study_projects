# Generated by Django 3.2 on 2021-04-29 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_app_test_1', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bd',
            name='price',
            field=models.FloatField(blank=True, default='Цена не указана', null=True),
        ),
    ]
