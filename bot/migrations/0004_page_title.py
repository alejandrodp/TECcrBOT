# Generated by Django 4.0 on 2022-02-06 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0003_page_mtime'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='title',
            field=models.TextField(default='???', max_length=512),
            preserve_default=False,
        ),
    ]
