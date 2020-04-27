from maintenance.models import *

class AssetTable():
    model = Asset
    verbose_name = "Asset"
    verbose_plural_name = "Assets"
    fields = ('name', 'tag', 'model__name','department__name')

class DepartmentTable():
    model = Department
    verbose_name = "Department"
    verbose_plural_name = "Departments"

class OrganizationTable():
    model = Organization
    verbose_name = "Organization"
    verbose_plural_name = "Organizations"

class ManufacturerTable():
    model = Manufacturer
    verbose_name = "Manufacturer"
    verbose_plural_name = "Manufacturers"

class ModelTable():
    model = Model
    fields = ('name', 'manufacturer__name')
    verbose_name = "Model"
    verbose_plural_name = "Models"
