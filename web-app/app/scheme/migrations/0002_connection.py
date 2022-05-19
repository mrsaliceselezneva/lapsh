# Generated by Django 4.0.4 on 2022-05-02 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheme', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Connection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Связь')),
                ('body', models.TextField(verbose_name='Определение')),
                ('image', models.ImageField(upload_to='scheme/connection', verbose_name='Рисунок')),
                ('mark', models.CharField(max_length=100, verbose_name='Обозначение')),
            ],
            options={
                'verbose_name': 'Связь',
                'verbose_name_plural': 'Связи',
            },
        ),
    ]
