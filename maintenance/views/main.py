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
import json

class Dashboard(LoginRequiredMixin, TemplateView):
    def get(self, request):
        return render(request, 'dashboard.html', {})

class Table(LoginRequiredMixin, TemplateView):
    tableObj = None

    def get(self, request, *args, **kwargs):
        assetQuerySet = self.tableObj.model.objects.order_by('-id').values()
        if hasattr(self.tableObj, 'fields'):
            assetQuerySet = self.tableObj.model.objects.order_by('-id').values('id', *self.tableObj.fields)
        paginatorObj = Paginator(assetQuerySet, 5)

        page_number = request.GET.get('page')
        page_obj = paginatorObj.get_page(page_number)

        return render(request, 'tables/generic.html', {'table': page_obj, 'tableObj': self.tableObj, 'paginatorObj': paginatorObj})

class TableForm(LoginRequiredMixin, TemplateView):
    formObj = None
    requestFormat = None

    def get(self, request, *args, **kwargs):
        return render(request, 'forms/generic.html', {'form': self.formObj})

    def post(self, request, *args, **kwargs):
        form = self.formObj(request.POST)

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
                return HttpResponseRedirect(self.formObj.Meta.baseUrl)
        else:
            if self.requestFormat == 'json':
                responseObj['valid'] = False
                responseObj['errors'] = form.errors

                return HttpResponse(json.dumps(responseObj))
            else:
                return render(request, 'forms/generic.html', {'form': form})

class DeleteTable(LoginRequiredMixin, TemplateView):
    tableObj = None

    def post(self, request, *args, **kwargs):
        objectList = request.POST.get('objects').split(',')

        self.tableObj.model.objects.filter(pk__in=objectList).delete()
        return HttpResponseRedirect('/')

class ViewTable(LoginRequiredMixin, TemplateView):
    tableObj = None

    def get(self, request, *args, **kwargs):
        objectId = kwargs['id']
        objectQuerySet = self.tableObj.model.objects.get(pk=objectId)

        fields = self.tableObj.model._meta.fields

        object = []

        for field in fields:
            if not field.name == 'id':
                data = getattr(objectQuerySet, field.name)
                objectDict = {
                    'name': field.verbose_name,
                    'value': data
                }
                if field.get_internal_type() == 'ForeignKey':
                    objectDict['link'] = '%sview/%s/' % (reverse(field.name), data.id)

                object.append(objectDict)

        return render(request, 'view/generic.html', {'object': object, 'tableObj': self.tableObj})

class Logout(TemplateView):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/login/')
