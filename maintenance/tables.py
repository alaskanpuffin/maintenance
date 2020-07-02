from .models import *
from .forms import *

class AssetTable():
    model = Asset
    form = AssetForm
    verbose_name = "Asset"
    verbose_plural_name = "Assets"
    url = 'asset'
    fields = ('name', 'tag', 'category__name', 'status', 'model__name', 'serial')
    search_fields = ('name', 'tag', 'serial')

class LicenseTable():
    model = License
    form = LicenseForm
    verbose_name = "License"
    verbose_plural_name = "Licenses"
    url = 'license'
    fields = ('name', 'status', 'expirationDate', 'department__name')
    search_fields = ('name', 'key')

class ComponentTable():
    model = Component
    form = ComponentForm
    verbose_name = "Component"
    verbose_plural_name = "Components"
    url = 'component'
    fields = ('name', 'tag', 'category__name', 'status', 'model__name')
    search_fields = ('name', 'tag')

class AccountTable():
    model = Account
    form = AccountForm
    verbose_name = "Account"
    verbose_plural_name = "Accounts"
    url = 'account'

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
    model = CustomUser
    form = UserForm
    fields = ('username', 'first_name', 'last_name', 'userId')
    verbose_name = "User"
    verbose_plural_name = "Users"
    url = 'user'
    search_fields = ('username', 'first_name', 'last_name')

class SupplierTable():
    model = Supplier
    form = SupplierForm
    verbose_name = "Supplier"
    verbose_plural_name = "Suppliers"
    fields = ('name',)
    url = 'supplier'

class AddressTable():
    model = Address
    form = AddressForm
    verbose_name = "Address"
    verbose_plural_name = "Addresses"
    url = 'address'

class PurchaseOrderRowTable():
    model = PurchaseOrderRow
    form = PurchaseOrderRowForm
    verbose_name = "Purchase Order Row"
    verbose_plural_name = "Purchase Order Rows"
    fields = ('name', 'purchaseOrder__purchaseOrderNumber','itemType', 'price', 'quantity', 'received')
    search_fields = ('name', 'purchaseOrder__purchaseOrderNumber')
    url = 'purchaseorderrow'

class PurchaseOrderTable():
    model = PurchaseOrder
    form = PurchaseOrderForm
    inline_models = [PurchaseOrderRowForm]
    download = 'purchaseorderreport'
    inline_fields = ('name', 'itemType', 'price', 'quantity', 'received')
    verbose_name = "Purchase Order"
    verbose_plural_name = "Purchase Orders"
    fields = ('purchaseOrderNumber', 'supplier__name', 'shippingAddress__name', 'billingAddress__name', 'requiredBy')
    url = 'purchaseorder'

class WorkOrderTable():
    model = WorkOrder
    form = WorkOrderForm
    verbose_name = "Work Order"
    verbose_plural_name = "Work Orders"
    fields = ('date', 'status', 'priority', 'type', 'requiredByDate', 'location')
    url = 'workorder'
