from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.shortcuts import render
from maintenance.models import *
from maintenance.forms import *
from django.core.paginator import Paginator
from django.urls import reverse

class Dashboard(TemplateView):
    def get(self, request):
        return render(request, 'templates/dashboard.html', {})

class Table(TemplateView):
    tableObj = None

    def get(self, request, *args, **kwargs):
        assetQuerySet = self.tableObj.model.objects.order_by('-id').values()
        if hasattr(self.tableObj, 'fields'):
            assetQuerySet = self.tableObj.model.objects.order_by('-id').values('id', *self.tableObj.fields)
        paginatorObj = Paginator(assetQuerySet, 5)

        page_number = request.GET.get('page')
        page_obj = paginatorObj.get_page(page_number)

        return render(request, 'templates/tables/generic.html', {'table': page_obj, 'tableObj': self.tableObj, 'paginatorObj': paginatorObj})

class AddTable(TemplateView):
    formObj = None

    def get(self, request, *args, **kwargs):
        return render(request, 'templates/forms/generic.html', {'form': self.formObj})

    def post(self, request, *args, **kwargs):
        form = self.formObj(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(self.formObj.Meta.redirect))
        else:
            return render(request, 'templates/forms/generic.html', {'form': form})

class ViewTable(TemplateView):
    tableObj = None

    def get(self, request, *args, **kwargs):
        objectId = kwargs['id']
        objectQuerySet = self.tableObj.model.objects.filter(pk=objectId)

        return render(request, 'templates/view/generic.html', {'object': objectQuerySet, 'tableObj': self.tableObj})
