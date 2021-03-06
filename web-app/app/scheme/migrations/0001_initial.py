# Generated by Django 4.0.4 on 2022-05-01 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Therm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Термин')),
                ('body', models.TextField(verbose_name='Определение')),
                ('image', models.ImageField(upload_to='scheme/', verbose_name='Рисунок')),
                ('mark', models.CharField(max_length=100, verbose_name='Обозначение')),
            ],
            options={
                'verbose_name': 'Термин',
                'verbose_name_plural': 'Термины',
            },
        ),
    ]
