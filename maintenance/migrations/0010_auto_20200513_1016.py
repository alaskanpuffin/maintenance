# Generated by Django 3.0.5 on 2020-05-13 18:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0009_auto_20200513_1015'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consumable',
            name='model',
        ),
        migrations.AddField(
            model_name='consumable',
            name='manufacturer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='maintenance.Manufacturer'),
        ),
    ]