from .models import *
from .forms import *

class AssetTable():
    model = Asset
    form = AssetForm
    verbose_name = "Asset"
    verbose_plural_name = "Assets"
    url = 'asset'
    fields = ('name', 'tag', 'model__name','department__name')
    search_fields = ('name', 'tag')

class DepartmentTable():
    model = Department
    form = DepartmentForm
    verbose_name = "Department"
    verbose_plural_name = "Departments"
    url = 'department'

class OrganizationTable():
    model = Organization
    form = OrganizationForm
    verbose_name = "Organization"
    verbose_plural_name = "Organizations"
    url = 'organization'

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
