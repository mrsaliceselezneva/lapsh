# Generated by Django 4.0.4 on 2022-05-18 19:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheme', '0010_rt_delete_info'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RT',
            new_name='RelationshipsTerms',
        ),
    ]
