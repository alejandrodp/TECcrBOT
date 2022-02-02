# Generated by Django 4.0 on 2022-01-31 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('ty', models.IntegerField()),
            ],
        ),
        migrations.AddConstraint(
            model_name='page',
            constraint=models.UniqueConstraint(fields=('id', 'ty'), name='page_id_type_unique'),
        ),
    ]