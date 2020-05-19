from django import forms
from django.forms import ModelForm
from django.utils import timezone
from django.forms import BaseModelFormSet
from .models import *
from .widgets import Select2, Select2NoAdd, Select2Multiple
from django.db.models import Q
from functools import reduce
from django.contrib.auth.hashers import make_password

class BootstrapFormMixin(forms.Form):
    def __init__(self,*args,**kwargs):
        super (BootstrapFormMixin,self ).__init__(*args,**kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['autocomplete'] = 'off'

        for field in self.fields:
            self.fields[field].widget.attrs['form'] = 'form-' + self.Meta.name

    def is_valid(self):
        ret = forms.Form.is_valid(self)
        for f in self.errors:
            self.fields[f].widget.attrs.update({'class': self.fields[f].widget.attrs.get('class', '') + ' is-invalid'})
        return ret


class PurchaseOrderRowForm(ModelForm, BootstrapFormMixin):
    class Meta:
        model = PurchaseOrderRow
        name = "Purchase Order Rows"
        fields = '__all__'

class PurchaseOrderForm(ModelForm, BootstrapFormMixin):
    def __init__(self,*args,**kwargs):
        super (PurchaseOrderForm,self ).__init__(*args,**kwargs)

        self.fields['requiredBy'].widget.attrs['class'] = 'form-control datepicker'

    class Meta:
        model = PurchaseOrder
        name = "Purchase Order"
        fields = '__all__'

class SiteForm(ModelForm, BootstrapFormMixin):
    class Meta:
        baseUrl = '/config/sites'
        model = Site
        name = "Site"
        fields = '__all__'

class AccountForm(ModelForm, BootstrapFormMixin):
    class Meta:
        model = Account
        name = "Account"
        fields = '__all__'

class CategoryForm(ModelForm, BootstrapFormMixin):
    class Meta:
        model = Category
        name = "Category"
        fields = '__all__'

class DepartmentForm(ModelForm, BootstrapFormMixin):
    class Meta:
        baseUrl = '/config/departments'
        model = Department
        name = "Department"
        fields = '__all__'

class ManufacturerForm(ModelForm, BootstrapFormMixin):
    class Meta:
        baseUrl = '/config/manufacturers'
        model = Manufacturer
        name = "Manufacturer"
        fields = '__all__'

class ModelsForm(ModelForm, BootstrapFormMixin):
    manufacturer = forms.ModelChoiceField(queryset=Manufacturer.objects.all(), widget=Select2(form=ManufacturerForm))

    class Meta:
        baseUrl = '/config/models'
        model = Model
        name = "Model"
        fields = '__all__'

class UserForm(ModelForm, BootstrapFormMixin):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)

    def save(self, commit=True):
        instance = super(UserForm, self).save(commit=False)
        if not self.cleaned_data['password'] == "":
            print(self.cleaned_data['password'])
            instance.password = make_password(self.cleaned_data['password'])
        else:
            if CustomUser.objects.filter(pk=instance.id).exists():
                userObj = CustomUser.objects.get(pk=instance.id)
                instance.password = userObj.password

        if commit:
            instance.save()
        return instance

    class Meta:
        model = CustomUser
        name = "User"
        fields = ('username', 'first_name', 'last_name', 'email', 'userId', 'password')

class AddressForm(ModelForm, BootstrapFormMixin):
    class Meta:
        model = Address
        name = "Address"
        fields = '__all__'

class SupplierForm(ModelForm, BootstrapFormMixin):
    address = forms.ModelChoiceField(queryset=Address.objects.all(), widget=Select2(form=AddressForm), required=False)

    class Meta:
        model = Supplier
        name = "Supplier"
        fields = '__all__'

class AssetForm(ModelForm, BootstrapFormMixin):
    site = forms.ModelChoiceField(queryset=Site.objects.all(), widget=Select2(form=SiteForm))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=Select2(form=CategoryForm))
    department = forms.ModelChoiceField(queryset=Department.objects.all(), widget=Select2(form=DepartmentForm), required=False)
    model = forms.ModelChoiceField(queryset=Model.objects.all(), widget=Select2(form=ModelsForm))
    user = forms.ModelChoiceField(queryset=CustomUser.objects.all(), widget=Select2(form=UserForm), required=False)
    purchaseOrder = forms.ModelChoiceField(queryset=PurchaseOrder.objects.all(), widget=Select2NoAdd(form=PurchaseOrderForm), required=False)
    supplier = forms.ModelChoiceField(queryset=Supplier.objects.all(), widget=Select2(form=SupplierForm), required=False)

    notes = forms.CharField( widget=forms.Textarea, required=False )

    def __init__(self,*args,**kwargs):
        super (AssetForm,self ).__init__(*args,**kwargs)

        self.fields['purchaseDate'].widget.attrs['class'] = 'form-control datepicker'
        self.fields['warrantyExpiration'].widget.attrs['class'] = 'form-control datepicker'

    class Meta:
        customTemplate = 'forms/asset.html'
        baseUrl = '/assets'
        model = Asset
        name = "Asset"
        fields = '__all__'

class ComponentForm(ModelForm, BootstrapFormMixin):
    site = forms.ModelChoiceField(queryset=Site.objects.all(), widget=Select2(form=SiteForm))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=Select2(form=CategoryForm))
    department = forms.ModelChoiceField(queryset=Department.objects.all(), widget=Select2(form=DepartmentForm), required=False)
    model = forms.ModelChoiceField(queryset=Model.objects.all(), widget=Select2(form=ModelsForm))
    user = forms.ModelChoiceField(queryset=CustomUser.objects.all(), widget=Select2(form=UserForm), required=False)
    asset = forms.ModelChoiceField(queryset=Asset.objects.all(), widget=Select2NoAdd(form=AssetForm), required=False)
    purchaseOrder = forms.ModelChoiceField(queryset=PurchaseOrder.objects.all(), widget=Select2NoAdd(form=PurchaseOrderForm), required=False)
    supplier = forms.ModelChoiceField(queryset=Supplier.objects.all(), widget=Select2(form=SupplierForm), required=False)

    notes = forms.CharField( widget=forms.Textarea, required=False )

    def __init__(self,*args,**kwargs):
        super (ComponentForm,self ).__init__(*args,**kwargs)

        self.fields['purchaseDate'].widget.attrs['class'] = 'form-control datepicker'
        self.fields['warrantyExpiration'].widget.attrs['class'] = 'form-control datepicker'

    class Meta:
        customTemplate = 'forms/component.html'
        model = Component
        name = "Component"
        fields = '__all__'

class LicenseForm(ModelForm, BootstrapFormMixin):
    site = forms.ModelChoiceField(queryset=Site.objects.all(), widget=Select2(form=SiteForm))
    department = forms.ModelChoiceField(queryset=Department.objects.all(), widget=Select2(form=DepartmentForm))
    user = forms.ModelChoiceField(queryset=CustomUser.objects.all(), widget=Select2(form=UserForm), required=False)
    asset = forms.ModelChoiceField(queryset=Asset.objects.all(), widget=Select2NoAdd(form=AssetForm), required=False)
    purchaseOrder = forms.ModelChoiceField(queryset=PurchaseOrder.objects.all(), widget=Select2NoAdd(form=PurchaseOrderForm), required=False)
    supplier = forms.ModelChoiceField(queryset=Supplier.objects.all(), widget=Select2(form=SupplierForm), required=False)
    manufacturer = forms.ModelChoiceField(queryset=Manufacturer.objects.all(), widget=Select2(form=ManufacturerForm))

    notes = forms.CharField( widget=forms.Textarea, required=False )

    def __init__(self,*args,**kwargs):
        super (LicenseForm,self ).__init__(*args,**kwargs)

        self.fields['expirationDate'].widget.attrs['class'] = 'form-control datepicker'
        self.fields['purchaseDate'].widget.attrs['class'] = 'form-control datepicker'

    class Meta:
        customTemplate = 'forms/license.html'
        model = License
        name = "License"
        fields = '__all__'

class ConsumableForm(ModelForm, BootstrapFormMixin):
    site = forms.ModelChoiceField(queryset=Site.objects.all(), widget=Select2(form=SiteForm))
    manufacturer = forms.ModelChoiceField(queryset=Manufacturer.objects.all(), widget=Select2(form=ManufacturerForm))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=Select2(form=CategoryForm))

    class Meta:
        model = Consumable
        name = "Consumable"
        fields = '__all__'

class ConsumableLedgerForm(ModelForm, BootstrapFormMixin):
    user = forms.ModelChoiceField(queryset=CustomUser.objects.all(), widget=Select2(form=UserForm), required=False)
    purchaseOrder = forms.ModelChoiceField(queryset=PurchaseOrder.objects.all(), widget=Select2NoAdd(form=PurchaseOrderForm), required=False)
    asset = forms.ModelChoiceField(queryset=Asset.objects.all(), widget=Select2NoAdd(form=AssetForm), required=False)
    consumable = forms.ModelChoiceField(queryset=Consumable.objects.all(), widget=Select2(form=ConsumableForm))

    class Meta:
        model = ConsumableLedger
        name = "Consumable Ledger"
        fields = '__all__'

class CheckoutForm(ModelForm, BootstrapFormMixin):
    validStatus = ['instore']
    user = forms.ModelChoiceField(queryset=CustomUser.objects.all(), widget=Select2(form=UserForm))
    assetSelect = forms.ModelMultipleChoiceField(queryset=Asset.objects.filter(reduce(lambda x, y: x | y, [Q(status=item) for item in validStatus])), widget=Select2Multiple(form=UserForm), required=False, label="Asset")

    class Meta:
        model = CheckoutLog
        name = "Batch Checkout"
        type = "checkout"
        fields = '__all__'

class CheckinForm(ModelForm, BootstrapFormMixin):
    validStatus = ['inuse']
    user = forms.ModelChoiceField(queryset=CustomUser.objects.all(), widget=Select2(form=UserForm))
    assetSelect = forms.ModelMultipleChoiceField(queryset=Asset.objects.filter(reduce(lambda x, y: x | y, [Q(status=item) for item in validStatus])), widget=Select2Multiple(form=UserForm), required=False, label="Asset")

    class Meta:
        model = CheckoutLog
        name = "Batch Checkin"
        type = "checkin"
        fields = '__all__'

class WorkOrderForm(ModelForm, BootstrapFormMixin):
    requestedBy = forms.ModelChoiceField(queryset=CustomUser.objects.all(), widget=Select2NoAdd(form=UserForm))
    assignedTo = forms.ModelChoiceField(queryset=CustomUser.objects.all(), widget=Select2NoAdd(form=UserForm), required=False)
    description = forms.CharField( widget=forms.Textarea, required=False )
    notes = forms.CharField( widget=forms.Textarea, required=False )

    def __init__(self,*args,**kwargs):
        super (WorkOrderForm,self ).__init__(*args,**kwargs)

        self.fields['requiredByDate'].widget.attrs['class'] = 'form-control datepicker'
        self.fields['date'].widget.attrs['class'] = 'form-control datepicker'

    class Meta:
        model = WorkOrder
        name = "Work Order"
        fields = '__all__'