# Generated by Django 4.0 on 2022-01-25 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='name',
            field=models.TextField(max_length=500, unique=True),
        ),
    ]
