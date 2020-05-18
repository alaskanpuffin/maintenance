# Generated by Django 3.0.5 on 2020-05-18 18:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0028_purchaseorder_purchaseordernumber'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseorder',
            name='billingAddress',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='billingAddress', to='maintenance.Address', verbose_name='Billing Address'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='requiredBy',
            field=models.DateField(default="2020-01-01", verbose_name='Required By Date'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='shippingAddress',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='shippingAddress', to='maintenance.Address', verbose_name='Shipping Address'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='purchaseOrderNumber',
            field=models.CharField(max_length=100, verbose_name='Purchase Order Number'),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='taxRate',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=3, verbose_name='Tax Rate'),
        ),
    ]
