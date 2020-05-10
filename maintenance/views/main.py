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

class Dashboard(LoginRequiredMixin, TemplateView):
    def get(self, request):
        data = {}

        data['asset_count'] = Asset.objects.count()

        return render(request, 'dashboard.html', {'data': data})

class CheckoutFormView(LoginRequiredMixin, TemplateView):
    def get(self, request):
        form = CheckoutForm

        return render(request, 'batch_checkout.html', {'form': form})

    def post(self, request):
        form = CheckoutForm(request.POST)

        if request.POST.get('checkout'):
            checkedout = True
        elif request.POST.get('checkin'):
            checkedout = False

        if form.is_valid():
            checkoutObj = form.save(commit=False)
            checkoutObj.checkedout = checkedout
            checkoutObj.save()
            form.save_m2m()
            
            if checkedout:
                form.cleaned_data['asset'].all().update(user=form.cleaned_data['user'], status='inuse')
            else:
                form.cleaned_data['asset'].all().update(user=None, department=None, status='instore')

            return HttpResponseRedirect(reverse('checkoutform'))
        else:
            return HttpResponse(form.errors.as_json())

class Table(LoginRequiredMixin, TemplateView):
    tableObj = None

    def get(self, request, *args, **kwargs):
        page_number = request.GET.get('page')

        self.tableObj = kwargs.get('tableObj')
        baseQuerySet = self.tableObj.model.objects.order_by('-updated')

        search = request.GET.get('search') # This function should be redone with a better solution.
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

    def get(self, request, *args, **kwargs):
        self.tableObj = kwargs.get('tableObj')
        form = self.tableObj.form

        if hasattr(form.Meta, 'customTemplate'):
            self.template = form.Meta.customTemplate

        if kwargs.get('id'):
            objectId = kwargs.get('id')
            querySet = self.tableObj.model.objects.get(pk=objectId)
            form = form(instance=querySet)

        return render(request, self.template, {'form': form, 'tableObj': self.tableObj})

    def post(self, request, *args, **kwargs):
        self.tableObj = kwargs.get('tableObj')
        form = self.tableObj.form(request.POST)

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
                return HttpResponseRedirect(reverse(self.tableObj.url + ':main'))
        else:
            if self.requestFormat == 'json':
                responseObj['valid'] = False
                responseObj['errors'] = form.errors

                return HttpResponse(json.dumps(responseObj))
            else:
                return render(request, self.template, {'form': form, 'tableObj': self.tableObj})

class DeleteTable(LoginRequiredMixin, TemplateView):
    tableObj = None

    def post(self, request, *args, **kwargs):
        self.tableObj = kwargs.get('tableObj')
        objectList = request.POST.get('objects').split(',')

        self.tableObj.model.objects.filter(pk__in=objectList).delete()
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
               print(field.choices)
               for choice in field.choices:
                   if data in choice[0]:
                       objectDict['value'] = choice[1]

            if field.get_internal_type() == 'ForeignKey' and data:
                objectDict['link'] = '%sview/%s/' % (reverse(field.name + ":main"), data.id)

            object.append(objectDict)

        return render(request, 'view/generic.html', {'object': object, 'querySet': objectQuerySet,'tableObj': self.tableObj})

class Logout(TemplateView):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/login/')
