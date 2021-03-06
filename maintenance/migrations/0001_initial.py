# Generated by Django 3.0.5 on 2020-05-19 19:52

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import localflavor.us.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('userId', models.CharField(max_length=100, verbose_name='User ID')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=300)),
                ('address', models.CharField(max_length=300)),
                ('city', models.CharField(max_length=100)),
                ('state', localflavor.us.models.USStateField(max_length=2)),
                ('zipCode', models.CharField(max_length=100, verbose_name='Zip Code')),
                ('phone', models.CharField(blank=True, max_length=100, null=True)),
                ('fax', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('tag', models.CharField(max_length=100, verbose_name='Tag/Barcode')),
                ('serial', models.CharField(blank=True, max_length=100, null=True)),
                ('location', models.CharField(blank=True, max_length=500, null=True)),
                ('notes', models.CharField(blank=True, max_length=1000, null=True)),
                ('status', models.CharField(choices=[('instore', 'In Store'), ('inuse', 'In Use'), ('onorder', 'On Order'), ('inrepair', 'In Repair'), ('discontinued', 'Discontinued'), ('disposed', 'Disposed')], default='instore', max_length=30)),
                ('purchaseDate', models.DateField(blank=True, null=True, verbose_name='Purchase Date')),
                ('purchaseCost', models.IntegerField(blank=True, null=True, verbose_name='Purchase Cost')),
                ('warrantyExpiration', models.DateField(blank=True, null=True, verbose_name='Warranty Expiration Date')),
                ('manufactureDate', models.DateField(blank=True, null=True, verbose_name='Manufacture Date')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Consumable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('quantity', models.IntegerField(default=0)),
                ('notes', models.CharField(blank=True, max_length=1000, null=True)),
                ('location', models.CharField(blank=True, max_length=500, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='maintenance.Category')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('purchaseOrderNumber', models.CharField(max_length=100, verbose_name='Purchase Order Number')),
                ('note', models.CharField(blank=True, max_length=1000, null=True)),
                ('requiredBy', models.DateField(verbose_name='Required By Date')),
                ('taxRate', models.DecimalField(decimal_places=2, default=0, max_digits=3, verbose_name='Tax Rate')),
                ('discount', models.IntegerField(default=0)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='maintenance.Account')),
                ('billingAddress', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='billingAddress', to='maintenance.Address', verbose_name='Billing Address')),
                ('shippingAddress', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='shippingAddress', to='maintenance.Address', verbose_name='Shipping Address')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WorkOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('date', models.DateField()),
                ('status', models.CharField(choices=[('requested', 'Requested'), ('open', 'Open'), ('onhold', 'On Hold'), ('inrepair', 'In Repair'), ('completed', 'Completed'), ('canceled', 'Canceled')], default='requested', max_length=30)),
                ('priority', models.CharField(choices=[('high', 'High'), ('medium', 'Medium'), ('low', 'Low')], default='medium', max_length=30)),
                ('type', models.CharField(choices=[('repair', 'Repair'), ('install', 'New Install'), ('preventive', 'Preventive Maintenance'), ('inspection', 'Inspection')], default='repair', max_length=30)),
                ('requiredByDate', models.DateField(verbose_name='Required By Date')),
                ('location', models.CharField(blank=True, max_length=500, null=True)),
                ('description', models.CharField(blank=True, max_length=4000, null=True)),
                ('assignedTo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='assignedTo', to=settings.AUTH_USER_MODEL, verbose_name='Assigned To')),
                ('requestedBy', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='requestedBy', to=settings.AUTH_USER_MODEL, verbose_name='Requested By')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='maintenance.Address')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PurchaseOrderRow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('itemType', models.CharField(choices=[('asset', 'Asset'), ('component', 'Component'), ('consumables', 'Consumables'), ('other', 'Other')], max_length=20, verbose_name='Type')),
                ('name', models.CharField(max_length=300)),
                ('price', models.FloatField()),
                ('quantity', models.IntegerField(default=1)),
                ('received', models.IntegerField(default=0)),
                ('purchaseOrder', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='maintenance.PurchaseOrder', verbose_name='Purchase Order')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='maintenance.Supplier'),
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('manufacturer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='maintenance.Manufacturer')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ConsumableLedger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('action', models.CharField(choices=[('in', 'Receive'), ('out', 'Checkout')], max_length=20)),
                ('quantity', models.IntegerField()),
                ('price', models.FloatField(blank=True, null=True)),
                ('externalPurchaseOrder', models.CharField(blank=True, max_length=300, null=True, verbose_name='External Purchase Order #')),
                ('asset', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='maintenance.Asset')),
                ('consumable', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='maintenance.Consumable')),
                ('purchaseOrder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='maintenance.PurchaseOrder', verbose_name='Linked Purchase Order')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='consumable',
            name='manufacturer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='maintenance.Manufacturer'),
        ),
        migrations.AddField(
            model_name='consumable',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='maintenance.Site'),
        ),
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('tag', models.CharField(max_length=100, verbose_name='Tag/Barcode')),
                ('serial', models.CharField(blank=True, max_length=100, null=True)),
                ('location', models.CharField(blank=True, max_length=500, null=True)),
                ('notes', models.CharField(blank=True, max_length=1000, null=True)),
                ('status', models.CharField(choices=[('instore', 'In Store'), ('inuse', 'In Use'), ('onorder', 'On Order'), ('inrepair', 'In Repair'), ('discontinued', 'Discontinued'), ('disposed', 'Disposed')], default='instore', max_length=30)),
                ('purchaseDate', models.DateField(blank=True, null=True, verbose_name='Purchase Date')),
                ('purchaseCost', models.IntegerField(blank=True, null=True, verbose_name='Purchase Cost')),
                ('warrantyExpiration', models.DateField(blank=True, null=True, verbose_name='Warranty Expiration Date')),
                ('manufactureDate', models.DateField(blank=True, null=True, verbose_name='Manufacture Date')),
                ('asset', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='maintenance.Asset')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='maintenance.Category')),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='maintenance.Department')),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='maintenance.Model')),
                ('purchaseOrder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='maintenance.PurchaseOrder', verbose_name='Linked Purchase Order')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='maintenance.Site')),
                ('supplier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='maintenance.Supplier')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CheckoutLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('checkedout', models.BooleanField()),
                ('asset', models.ManyToManyField(to='maintenance.Asset')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='asset',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='maintenance.Category'),
        ),
        migrations.AddField(
            model_name='asset',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='maintenance.Department'),
        ),
        migrations.AddField(
            model_name='asset',
            name='model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='maintenance.Model'),
        ),
        migrations.AddField(
            model_name='asset',
            name='purchaseOrder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='maintenance.PurchaseOrder', verbose_name='Linked Purchase Order'),
        ),
        migrations.AddField(
            model_name='asset',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='maintenance.Site'),
        ),
        migrations.AddField(
            model_name='asset',
            name='supplier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='maintenance.Supplier'),
        ),
        migrations.AddField(
            model_name='asset',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
