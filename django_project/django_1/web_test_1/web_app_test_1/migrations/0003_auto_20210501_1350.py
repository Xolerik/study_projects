# Generated by Django 3.2 on 2021-05-01 13:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web_app_test_1', '0002_alter_bd_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rubric',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=20, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Рубрика',
                'verbose_name_plural': 'Рубрики',
                'ordering': ['name'],
            },
        ),
        migrations.AlterModelOptions(
            name='bd',
            options={'ordering': ['-published'], 'verbose_name': 'Объявление', 'verbose_name_plural': 'Объявления'},
        ),
        migrations.AlterField(
            model_name='bd',
            name='content',
            field=models.TextField(blank=True, null=True, verbose_name='Описание товара'),
        ),
        migrations.AlterField(
            model_name='bd',
            name='price',
            field=models.FloatField(blank=True, null=True, verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='bd',
            name='published',
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата публикации0'),
        ),
        migrations.AlterField(
            model_name='bd',
            name='title',
            field=models.CharField(max_length=50, verbose_name='Наименование товара'),
        ),
        migrations.AddField(
            model_name='bd',
            name='rubric',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='web_app_test_1.rubric', verbose_name='Рубрика'),
        ),
    ]
