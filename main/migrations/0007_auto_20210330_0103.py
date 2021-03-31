# Generated by Django 3.1.4 on 2021-03-29 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20210330_0054'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Категория расходов', 'verbose_name_plural': 'Категории расходов'},
        ),
        migrations.AlterModelOptions(
            name='expense',
            options={'verbose_name': 'Расход', 'verbose_name_plural': 'Расходы'},
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'verbose_name': 'Проект', 'verbose_name_plural': 'Проекты'},
        ),
        migrations.AlterField(
            model_name='project',
            name='ceremony_place',
            field=models.CharField(max_length=200),
        ),
    ]