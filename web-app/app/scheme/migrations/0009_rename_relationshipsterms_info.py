# Generated by Django 4.0.4 on 2022-05-18 19:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheme', '0008_remove_relationshipsterms_title'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RelationshipsTerms',
            new_name='Info',
        ),
    ]
