# Generated by Django 4.0 on 2022-02-02 02:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0002_rolety_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='location',
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='directory.location'),
        ),
    ]
