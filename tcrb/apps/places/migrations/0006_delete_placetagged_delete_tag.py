# Generated by Django 4.0 on 2022-04-17 13:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0005_remove_edition_editor_remove_edition_place_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PlaceTagged',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]