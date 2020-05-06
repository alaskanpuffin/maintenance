from django import forms
from django.forms import ModelForm
from django.utils import timezone
from django.forms import BaseModelFormSet
from .models import *
from .widgets import Select2

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

class OrganizationForm(ModelForm, BootstrapFormMixin):
    class Meta:
        baseUrl = '/config/organizations'
        model = Organization
        name = "Organization"
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
    class Meta:
        baseUrl = '/config/users'
        model = OrganizationUsers
        name = "User"
        fields = '__all__'

class AssetForm(ModelForm, BootstrapFormMixin):
    organization = forms.ModelChoiceField(queryset=Organization.objects.all(), widget=Select2(form=OrganizationForm))
    department = forms.ModelChoiceField(queryset=Department.objects.all(), widget=Select2(form=DepartmentForm))
    model = forms.ModelChoiceField(queryset=Model.objects.all(), widget=Select2(form=ModelsForm))
    user = forms.ModelChoiceField(queryset=OrganizationUsers.objects.all(), widget=Select2(form=UserForm))

    def __init__(self,*args,**kwargs):
        super (AssetForm,self ).__init__(*args,**kwargs)

        self.fields['purchaseDate'].widget.attrs['class'] = 'form-control datepicker'

    class Meta:
        baseUrl = '/assets'
        model = Asset
        name = "Asset"
        fields = '__all__'
