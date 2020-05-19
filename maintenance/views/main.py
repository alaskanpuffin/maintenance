from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.urls import reverse
from django.views.generic import TemplateView
from django.shortcuts import render
from maintenance.models import *
from maintenance.forms import *
from django.core.paginator import Paginator
from django.urls import reverse
from django.core import serializers
from django.db.models import Q
import json
from django.contrib import messages
from django.db.models import ProtectedError
from django.forms import inlineformset_factory


class Dashboard(LoginRequiredMixin, TemplateView):
    def get(self, request):
        data = {}

        data['asset_count'] = Asset.objects.count()
        data['component_count'] = Component.objects.count()
        data['consumable_count'] = Consumable.objects.count()

        return render(request, 'dashboard.html', {'data': data})


class CheckoutFormView(LoginRequiredMixin, TemplateView):
    objForm = None

    def get(self, request, *args, **kwargs):
        form = kwargs.get('objForm')

        return render(request, 'batch_checkout.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = kwargs.get('objForm')(request.POST)

        if form.Meta.type == "checkout":
            checkedout = True
        elif form.Meta.type == "checkin":
            checkedout = False

        if form.is_valid():
            checkoutObj = form.save(commit=False)
            checkoutObj.checkedout = checkedout
            checkoutObj.save()
            form.save_m2m()

            if checkedout:
                form.cleaned_data['asset'].all().update(
                    user=form.cleaned_data['user'], status='inuse')
                messages.success(request, "The selected assets have been checked out.")
                return HttpResponseRedirect(reverse('checkoutform'))
            else:
                form.cleaned_data['asset'].all().update(
                    user=None, department=None, status='instore')
                messages.success(request, "The selected assets have been checked in.")
                return HttpResponseRedirect(reverse('checkinform'))
        else:
            for error in form.errors:
                messages.error(request, "An error has occured: %s" % error)
            return HttpResponseRedirect(reverse('asset:main'))


class Table(LoginRequiredMixin, TemplateView):
    tableObj = None

    def get(self, request, *args, **kwargs):
        page_number = request.GET.get('page')

        self.tableObj = kwargs.get('tableObj')
        baseQuerySet = self.tableObj.model.objects.order_by('-created')

        # This function should be redone with a better solution.
        search = request.GET.get('search')
        if search:
            queryparameters = ""
            for field in self.tableObj.search_fields:
                queryparameters += " Q(%s__contains=search) |" % (field,)

            query = "baseQuerySet.filter(%s)" % queryparameters[:-1]
            baseQuerySet = eval(query)

        objectQuerySet = baseQuerySet.values()
        if hasattr(self.tableObj, 'fields'):
            objectQuerySet = baseQuerySet.values('id', *self.tableObj.fields)

        object = []
        for row in objectQuerySet:
            rowArray = []
            for key, value in row.items():
                objectDict = {
                    'name': key,
                    'value': value
                }

                if value == 'instore':
                    objectDict['value'] = 'In Store'
                elif value == 'inuse':
                    objectDict['value'] = 'In Use'
                elif value == 'inrepair':
                    objectDict['value'] = 'In Repair'
                elif value == 'onorder':
                    objectDict['value'] = 'On Order'

                if not key.lower() in ['id', 'created', 'updated']:
                    rowArray.append(objectDict)
            object.append({'data': rowArray, 'id': row['id']})

        paginatorObj = Paginator(object, 25)
        page_obj = paginatorObj.get_page(page_number)

        return render(request, 'tables/generic.html', {'table': page_obj, 'tableObj': self.tableObj, 'paginatorObj': paginatorObj})


class TableForm(LoginRequiredMixin, TemplateView):
    tableObj = None
    requestFormat = None
    template = 'forms/generic.html'

    def generateFormset(self):
        formsets = []
        if hasattr(self.tableObj, 'inline_models'):
            for inline_model in self.tableObj.inline_models:
                formset = inlineformset_factory(self.tableObj.model, inline_model.Meta.model, fields=self.tableObj.inline_fields)

                formsetDict = {
                    'formset': formset,
                    'name': inline_model.Meta.name,
                    'model': inline_model.Meta.model
                }
                formsets.append(formsetDict)
        return formsets

    def get(self, request, *args, **kwargs):
        self.tableObj = kwargs.get('tableObj')
        form = self.tableObj.form

        formsets = self.generateFormset()
        
        if hasattr(form.Meta, 'customTemplate'):
            self.template = form.Meta.customTemplate

        if kwargs.get('id'):
            objectId = kwargs.get('id')
            querySet = self.tableObj.model.objects.get(pk=objectId)
            form = form(instance=querySet)
            formsets = self.generateFormset()

        return render(request, self.template, {'form': form, 'formsets': formsets, 'tableObj': self.tableObj})

    def post(self, request, *args, **kwargs):
        self.tableObj = kwargs.get('tableObj')
        form = self.tableObj.form(request.POST)

        formsets = self.generateFormset()

        if hasattr(form.Meta, 'customTemplate'):
            self.template = form.Meta.customTemplate

        if kwargs.get('id'):
            objectId = kwargs.get('id')
            querySet = self.tableObj.model.objects.get(pk=objectId)
            form = self.tableObj.form(request.POST, instance=querySet)

        if request.GET.get('format'):
            self.requestFormat = request.GET.get('format')

        responseObj = {}

        if form.is_valid():
            savedFormObj = form.save()
            responseObj['valid'] = True
            responseObj['pk'] = savedFormObj.pk
            responseObj['name'] = savedFormObj.__str__()

            if self.requestFormat == 'json':
                return HttpResponse(json.dumps(responseObj))
            else:
                messages.success(request, "A record in %s has been successfully created." % self.tableObj.verbose_name)
                return HttpResponseRedirect(reverse(self.tableObj.url + ':main'))
        else:
            if self.requestFormat == 'json':
                responseObj['valid'] = False
                responseObj['errors'] = form.errors

                return HttpResponse(json.dumps(responseObj))
            else:
                return render(request, self.template, {'form': form, 'formsets': formsets, 'tableObj': self.tableObj})


class DeleteTable(LoginRequiredMixin, TemplateView):
    tableObj = None

    def get(self, request, *args, **kwargs):
        self.tableObj = kwargs.get('tableObj')

        return HttpResponseRedirect(reverse(self.tableObj.url + ':main'))

    def post(self, request, *args, **kwargs):
        self.tableObj = kwargs.get('tableObj')
        objectList = request.POST.get('objects').split(',')

        try:
            deleteObj = self.tableObj.model.objects.filter(pk__in=objectList)
            for row in deleteObj:
                messages.success(request, '%s has been deleted.' % row.__str__())
                
            deleteObj.delete()
            return HttpResponseRedirect(reverse(self.tableObj.url + ':main'))
        except ProtectedError as e:
            messages.error(request, str(e))
            return HttpResponseRedirect(reverse(self.tableObj.url + ':main'))


class ViewTable(LoginRequiredMixin, TemplateView):
    tableObj = None

    def get(self, request, *args, **kwargs):
        self.tableObj = kwargs.get('tableObj')
        objectId = kwargs['id']
        objectQuerySet = self.tableObj.model.objects.get(pk=objectId)

        fields = self.tableObj.model._meta.fields

        object = []

        for field in fields:
            data = getattr(objectQuerySet, field.name)
            objectDict = {
                'name': field.verbose_name,
                'value': data
            }

            if not field.choices == None:
                for choice in field.choices:
                    if data in choice[0]:
                        objectDict['value'] = choice[1]

            if field.get_internal_type() == 'ForeignKey' and data:
                try:
                    objectDict['link'] = '%sview/%s/' % (
                        reverse(field.name.lower() + ":main"), data.id)
                except:
                    pass

            object.append(objectDict)

        return render(request, 'view/generic.html', {'object': object, 'querySet': objectQuerySet, 'tableObj': self.tableObj})


class Logout(TemplateView):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/login/')
