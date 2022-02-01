# Generated by Django 4.0 on 2022-01-28 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=500, unique=True)),
                ('description', models.TextField(max_length=5000)),
                ('link', models.URLField(max_length=500)),
                ('contact', models.TextField(max_length=5000)),
            ],
        ),
    ]
