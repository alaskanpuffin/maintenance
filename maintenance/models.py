from django.contrib.auth.models import AbstractUser
from django.db import models

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
        return self.name
