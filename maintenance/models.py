from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    pass
    # add additional fields in here

    def __str__(self):
        return self.username

class Organization(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Manufacturer(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Model(models.Model):
    name = models.CharField(max_length=100)
    manufacturer = models.ForeignKey(
        'Manufacturer',
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return self.name

class Asset(models.Model):
    name = models.CharField(max_length=100)
    tag = models.CharField(max_length=100)
    serial = models.CharField(max_length=100)
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

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
