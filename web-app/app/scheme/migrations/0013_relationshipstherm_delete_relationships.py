# Generated by Django 4.0.4 on 2022-05-19 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheme', '0012_relationships_delete_relationshipsterms'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelationshipsTherm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('therm_id', models.IntegerField(verbose_name='первый термин')),
                ('title', models.CharField(max_length=100, verbose_name='первый термин')),
                ('web', models.CharField(max_length=100, verbose_name='ссылка')),
                ('therm_title', models.CharField(max_length=100, verbose_name='второй термин')),
                ('connection', models.CharField(max_length=100, verbose_name='Связь терминов')),
            ],
            options={
                'verbose_name': 'Связь терминов',
                'verbose_name_plural': 'Связи терминов',
            },
        ),
        migrations.DeleteModel(
            name='Relationships',
        ),
    ]