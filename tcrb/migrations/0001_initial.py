# Generated by Django 4.0 on 2022-02-25 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ty', models.IntegerField()),
                ('title', models.TextField(max_length=512)),
                ('mtime', models.DateField(null=True)),
            ],
        ),
    ]
