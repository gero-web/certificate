# Generated by Django 3.2.16 on 2023-01-23 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_pdfcertificate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pdfcertificate',
            name='key',
            field=models.SlugField(unique=True),
        ),
    ]
