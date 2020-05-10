from .models import *
from .forms import *

class AssetTable():
    model = Asset
    form = AssetForm
    verbose_name = "Asset"
    verbose_plural_name = "Assets"
    url = 'asset'
    fields = ('name', 'tag', 'status', 'model__name')
    search_fields = ('name', 'tag')

class DepartmentTable():
    model = Department
    form = DepartmentForm
    verbose_name = "Department"
    verbose_plural_name = "Departments"
    url = 'department'

class SiteTable():
    model = Site
    form = SiteForm
    verbose_name = "Site"
    verbose_plural_name = "Sites"
    url = 'site'

class ManufacturerTable():
    model = Manufacturer
    form = ManufacturerForm
    verbose_name = "Manufacturer"
    verbose_plural_name = "Manufacturers"
    url = 'manufacturer'

class ModelTable():
    model = Model
    form = ModelsForm
    fields = ('name', 'manufacturer__name')
    verbose_name = "Model"
    verbose_plural_name = "Models"
    url = 'model'

class UserTable():
    model = OrganizationUsers
    form = UserForm
    fields = ('firstName', 'lastName')
    verbose_name = "User"
    verbose_plural_name = "Users"
    url = 'user'
    search_fields = ('firstName', 'lastName')

class SupplierTable():
    model = Supplier
    form = SupplierForm
    verbose_name = "Supplier"
    verbose_plural_name = "Suppliers"
    url = 'supplier'
