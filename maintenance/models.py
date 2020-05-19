from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from localflavor.us.models import USStateField

class DefaultMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class CustomUser(AbstractUser, DefaultMixin):
    userId = models.CharField(max_length=100, verbose_name="User ID")

    def __str__(self):
        return self.first_name + " " + self.last_name + " - " + self.userId

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

class Accounts(DefaultMixin):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Address(DefaultMixin):
    name = models.CharField(max_length=300)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    state = USStateField()
    zipCode = models.CharField(max_length=100, verbose_name="Zip Code")
    phone = models.CharField(max_length=100, blank=True, null=True)
    fax = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    def __str__(self):
        return self.name

class Supplier(DefaultMixin):
    name = models.CharField(max_length=100)
    address = models.ForeignKey(
        'Address',
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )

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

class Asset(DefaultMixin):
    # General Information
    name = models.CharField(max_length=100)
    tag = models.CharField(max_length=100, verbose_name="Tag/Barcode")
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
        ('onorder', 'On Order'),
        ('inrepair', 'In Repair'),
        ('discontinued', 'Discontinued'),
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
    purchaseCost = models.IntegerField(blank=True, null=True, verbose_name="Purchase Cost")
    purchaseOrder = models.ForeignKey(
        'purchaseOrder',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="Linked Purchase Order"
    )

    # Lifetime Information
    warrantyExpiration = models.DateField(verbose_name="Warranty Expiration Date", blank=True, null=True)
    manufactureDate = models.DateField(verbose_name="Manufacture Date", blank=True, null=True)

    # Checkout Information
    user = models.ForeignKey(
        'CustomUser',
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
        return self.name + " - " + self.model.manufacturer.name + " " + self.model.name + " - " + self.tag

class Component(DefaultMixin):
    # General Information
    name = models.CharField(max_length=100)
    tag = models.CharField(max_length=100, verbose_name="Tag/Barcode")
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
        ('onorder', 'On Order'),
        ('inrepair', 'In Repair'),
        ('discontinued', 'Discontinued'),
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
    purchaseCost = models.IntegerField(blank=True, null=True, verbose_name="Purchase Cost")
    purchaseOrder = models.ForeignKey(
        'purchaseOrder',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="Linked Purchase Order"
    )
    

    # Lifetime Information
    warrantyExpiration = models.DateField(verbose_name="Warranty Expiration Date", blank=True, null=True)
    manufactureDate = models.DateField(verbose_name="Manufacture Date", blank=True, null=True)

    # Checkout Information
    user = models.ForeignKey(
        'CustomUser',
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
    asset = models.ForeignKey(
        'Asset',
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
    category = models.ForeignKey(
        'Category',
        on_delete=models.PROTECT,
    )
    quantity = models.IntegerField(default=0)
    notes = models.CharField(max_length=1000, blank=True, null=True)
    location = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.manufacturer.name + " " + self.name

class ConsumableLedger(DefaultMixin):
    consumable = models.ForeignKey(
        'Consumable',
        on_delete=models.PROTECT,
    )
    ACTION_CHOICES = [
        ('in', 'Receive'),
        ('out', 'Checkout'),
    ]
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    quantity = models.IntegerField()

    # Purchasing Information
    price = models.FloatField(blank=True, null=True)
    purchaseOrder = models.ForeignKey(
        'purchaseOrder',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="Linked Purchase Order"
    )
    externalPurchaseOrder = models.CharField(max_length=300, blank=True, null=True, verbose_name="External Purchase Order #")

    # Checkout Information
    user = models.ForeignKey(
        'CustomUser',
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
        'CustomUser',
        on_delete=models.PROTECT,
    )
    asset = models.ManyToManyField(Asset)
    checkedout = models.BooleanField()

    def __str__(self):
        return self.user.firstName

# Purchasing
class PurchaseOrder(DefaultMixin):
    purchaseOrderNumber = models.CharField(max_length=100, verbose_name="Purchase Order Number")
    supplier = models.ForeignKey(
        'Supplier',
        on_delete=models.PROTECT
    )
    note = models.CharField(max_length=1000, blank=True, null=True)
    shippingAddress = models.ForeignKey(
        'Address',
        on_delete=models.PROTECT,
        verbose_name="Shipping Address",
        related_name="shippingAddress"
    )
    billingAddress = models.ForeignKey(
        'Address',
        on_delete=models.PROTECT,
        verbose_name="Billing Address",
        related_name="billingAddress"
    )
    requiredBy = models.DateField(verbose_name="Required By Date")
    taxRate = models.DecimalField(max_digits=3, decimal_places=2, default=0, verbose_name="Tax Rate")
    discount = models.IntegerField(default=0)

    def __str__(self):
        return self.purchaseOrderNumber

class PurchaseOrderRow(DefaultMixin):
    purchaseOrder = models.ForeignKey(
        'PurchaseOrder',
        on_delete=models.PROTECT,
        verbose_name="Purchase Order"
    )

    TYPE_CHOICES = [
        ('asset', 'Asset'),
        ('component', 'Component'),
        ('consumables', 'Consumables'),
        ('other', 'Other'),
    ]
    itemType = models.CharField(max_length=20, verbose_name="Type", choices=TYPE_CHOICES)
    name = models.CharField(max_length=300)
    price = models.FloatField()
    quantity = models.IntegerField(default=1)
    received = models.IntegerField(default=0)

    def __str__(self):
        return self.name

# Maintenance Work Orders
class WorkOrder(DefaultMixin):
    # General Information
    date = models.DateField()
    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('open', 'Open'),
        ('onhold', 'On Hold'),
        ('inrepair', 'In Repair'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="requested")
    PRIORITY_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]
    priority = models.CharField(max_length=30, choices=PRIORITY_CHOICES, default="medium")
    TYPE_CHOICES = [
        ('repair', 'Repair'),
        ('install', 'New Install'),
        ('preventive', 'Preventive Maintenance'),
        ('inspection', 'Inspection'),
    ]
    type = models.CharField(max_length=30, choices=TYPE_CHOICES, default="repair")
    requiredByDate = models.DateField(verbose_name="Required By Date")

    # Users
    requestedBy = models.ForeignKey(
        'CustomUser',
        on_delete=models.PROTECT,
        related_name="requestedBy",
        verbose_name="Requested By"
    )
    assignedTo = models.ForeignKey(
        'CustomUser',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="assignedTo",
        verbose_name="Assigned To"
    )

    # WO Details
    location = models.CharField(max_length=500, blank=True, null=True)
    description = models.CharField(max_length=5000, blank=True, null=True)

    def __str__(self):
        return "WO%s" % (self.id,)