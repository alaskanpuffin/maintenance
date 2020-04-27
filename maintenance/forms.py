from django import forms
from django.forms import ModelForm
from django.utils import timezone
from django.forms import BaseModelFormSet
from .models import *

class BootstrapFormMixin(forms.Form):
    def __init__(self,*args,**kwargs):
        super (BootstrapFormMixin,self ).__init__(*args,**kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['autocomplete'] = 'off'

    def is_valid(self):
        ret = forms.Form.is_valid(self)
        for f in self.errors:
            self.fields[f].widget.attrs.update({'class': self.fields[f].widget.attrs.get('class', '') + ' is-invalid'})
        return ret

class AssetForm(ModelForm, BootstrapFormMixin):
    class Meta:
        redirect = '/assets/'
        model = Asset
        name = "Asset"
        fields = '__all__'

class OrganizationForm(ModelForm, BootstrapFormMixin):
    class Meta:
        redirect = 'organizations'
        model = Organization
        name = "Organization"
        fields = '__all__'

class DepartmentForm(ModelForm, BootstrapFormMixin):
    class Meta:
        redirect = 'departments'
        model = Department
        name = "Department"
        fields = '__all__'

class ManufacturerForm(ModelForm, BootstrapFormMixin):
    class Meta:
        redirect = 'manufacturers'
        model = Manufacturer
        name = "Manufacturer"
        fields = '__all__'

class ModelsForm(ModelForm, BootstrapFormMixin):
    class Meta:
        redirect = 'models'
        model = Model
        name = "Model"
        fields = '__all__'
