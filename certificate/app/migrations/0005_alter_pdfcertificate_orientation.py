# Generated by Django 3.2.16 on 2023-01-26 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_pdfcertificate_orientation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pdfcertificate',
            name='orientation',
            field=models.CharField(max_length=255),
        ),
    ]
