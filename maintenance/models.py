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

class Organization(DefaultMixin):
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
    name = models.CharField(max_length=100)
    tag = models.CharField(max_length=100)
    serial = models.CharField(max_length=100, blank=True, null=True)
    purchaseDate = models.DateField(verbose_name="Purchase Date")

    organization = models.ForeignKey(
        'Organization',
        on_delete=models.PROTECT,
    )
    department = models.ForeignKey(
        'Department',
        on_delete=models.PROTECT,
    )
    model = models.ForeignKey(
        'Model',
        on_delete=models.PROTECT,
    )
    user = models.ForeignKey(
        'OrganizationUsers',
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name
