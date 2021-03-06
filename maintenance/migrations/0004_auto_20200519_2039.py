# Generated by Django 3.0.5 on 2020-05-19 20:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0003_auto_20200519_2037'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asset',
            name='ownerDepartment',
        ),
        migrations.AddField(
            model_name='asset',
            name='checkoutDepartment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='checkoutDepartment', to='maintenance.Department'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='department',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='maintenance.Department'),
            preserve_default=False,
        ),
    ]
