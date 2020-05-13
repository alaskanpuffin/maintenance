from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

class DefaultMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class CustomUser(AbstractUser):
    pass
    # add additional fields in here

    def __str__(self):
        return self.username

class Site(DefaultMixin):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Category(DefaultMixin):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Department(DefaultMixin):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Manufacturer(DefaultMixin):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Supplier(DefaultMixin):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Model(DefaultMixin):
    name = models.CharField(max_length=100)
    manufacturer = models.ForeignKey(
        'Manufacturer',
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return self.manufacturer.name + " " + self.name

class OrganizationUsers(DefaultMixin):
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)

    def __str__(self):
        return self.firstName + " " + self.lastName

class Asset(DefaultMixin):
    # General Information
    name = models.CharField(max_length=100)
    tag = models.CharField(max_length=100)
    site = models.ForeignKey(
        'Site',
        on_delete=models.PROTECT,
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.PROTECT,
    )
    model = models.ForeignKey(
        'Model',
        on_delete=models.PROTECT,
    )
    serial = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=500, blank=True, null=True)
    notes = models.CharField(max_length=1000, blank=True, null=True)

    STATUS_CHOICES = [
        ('instore', 'In Store'),
        ('inuse', 'In Use'),
        ('inrepair', 'In Repair'),
        ('disposed', 'Disposed'),
    ]
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="instore")

    # Purchasing Information
    purchaseDate = models.DateField(verbose_name="Purchase Date", blank=True, null=True)
    supplier = models.ForeignKey(
        'Supplier',
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )
    purchaseCost = models.IntegerField(blank=True, null=True)

    # Lifetime Information
    warrantyExpiration = models.DateField(verbose_name="Warranty Expiration Date", blank=True, null=True)
    manufactureDate = models.DateField(verbose_name="Manufacture Date", blank=True, null=True)

    # Checkout Information
    user = models.ForeignKey(
        'OrganizationUsers',
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )
    department = models.ForeignKey(
        'Department',
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name + " - " + self.tag

class Consumable(DefaultMixin):
    # General Information
    name = models.CharField(max_length=100)
    site = models.ForeignKey(
        'Site',
        on_delete=models.PROTECT,
    )
    manufacturer = models.ForeignKey(
        'Manufacturer',
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )
    quantity = models.IntegerField(default=0)
    notes = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.manufacturer.name + " " + self.name

class ConsumableLedger(DefaultMixin):
    consumable = models.ForeignKey(
        'Consumable',
        on_delete=models.PROTECT,
    )
    ACTION_CHOICES = [
        ('in', 'In'),
        ('out', 'Out'),
    ]
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    quantity = models.IntegerField()

    # Purchasing Information
    price = models.IntegerField(blank=True, null=True)
    purchaseOrderId = models.CharField(max_length=100, blank=True, null=True)

    # Checkout Information
    user = models.ForeignKey(
        'OrganizationUsers',
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )
    asset = models.ForeignKey(
        'Asset',
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )

@receiver(pre_save, sender=ConsumableLedger, dispatch_uid="update_consumable_quantity")
def update_quantity(sender, instance, **kwargs):
    if instance.id == None:
        if instance.action == 'in':
            instance.consumable.quantity += instance.quantity
        elif instance.action == 'out':
            instance.consumable.quantity -= instance.quantity
    else:
        previous = ConsumableLedger.objects.get(pk=instance.id)
        if instance.action == 'in':
            instance.consumable.quantity += instance.quantity - previous.quantity
        elif instance.action == 'out':
            instance.consumable.quantity -= instance.quantity - previous.quantity

    instance.consumable.save()

@receiver(post_delete, sender=ConsumableLedger, dispatch_uid="update_deleted_consumable_quantity")
def update_deleted_quantity(sender, instance, **kwargs):
    if instance.action == 'in':
        instance.consumable.quantity -= instance.quantity
    elif instance.action == 'out':
        instance.consumable.quantity += instance.quantity
    instance.consumable.save()

class CheckoutLog(DefaultMixin):
    user = models.ForeignKey(
        'OrganizationUsers',
        on_delete=models.PROTECT,
    )
    asset = models.ManyToManyField(Asset)
    checkedout = models.BooleanField()

    def __str__(self):
        return self.user.firstName

# Purchasing
# class PurchaseOrder(DefaultMixin):
#     supplier = models.ForeignKey(
#         'Supplier',
#         on_delete=models.PROTECT
#     )
#     taxRate = models.DecimalField(max_digits=3, decimal_places=2)
#     discount = models.IntegerField(default=0)

# class PurchaseOrderRow(DefaultMixin):
#     purchaseOrder = models.ForeignKey(
#         'PurchaseOrder',
#         on_delete=models.PROTECT
#     )
#     price = models.IntegerField()
#     quantity = models.IntegerField(default=1)