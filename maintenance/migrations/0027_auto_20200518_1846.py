# Generated by Django 3.0.5 on 2020-05-18 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0026_auto_20200518_1845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='note',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
