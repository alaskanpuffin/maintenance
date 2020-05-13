from .models import *
from .forms import *

class AssetTable():
    model = Asset
    form = AssetForm
    verbose_name = "Asset"
    verbose_plural_name = "Assets"
    url = 'asset'
    fields = ('name', 'tag', 'category__name', 'status', 'model__name')
    search_fields = ('name', 'tag')

class ConsumableTable():
    model = Consumable
    form = ConsumableForm
    verbose_name = "Consumable"
    verbose_plural_name = "Consumables"
    url = 'consumable'
    fields = ('name', 'manufacturer__name', 'site__name', 'quantity')
    search_fields = ('name',)

class ConsumableLedgerTable():
    model = ConsumableLedger
    form = ConsumableLedgerForm
    verbose_name = "Consumable Ledger Entry"
    verbose_plural_name = "Consumable Ledger"
    url = 'consumableledger'
    fields = ('consumable__name', 'action', 'quantity')
    search_fields = ('consumable__name', 'purchaseOrderId')

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

class CategoryTable():
    model = Category
    form = CategoryForm
    verbose_name = "Category"
    verbose_plural_name = "Categories"
    url = 'category'

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
