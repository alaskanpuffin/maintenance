# Generated by Django 3.0.5 on 2020-05-19 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0008_license_manufacturer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='license',
            name='key',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='License Key'),
        ),
    ]
