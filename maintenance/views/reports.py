from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import render
from maintenance.models import *
from maintenance.forms import *


class PurchaseOrderReport(LoginRequiredMixin, TemplateView):
    def get(self, request, id=None):
        purchaseOrderObj = PurchaseOrder.objects.get(pk=id)
        purchaseOrderRowObj = PurchaseOrderRow.objects.filter(purchaseOrder=purchaseOrderObj).values()
        total = 0

        for row in purchaseOrderRowObj:
            total += row['price'] * row['quantity']
            
            row['total'] = '$'  + str((row['price'] * row['quantity']))
            row['price'] = '$'  + str(row['price'])

        subtotal = '$' + str(total)
        shipping = '$' + str(purchaseOrderObj.shipping)
        discount = '$' + str(purchaseOrderObj.discount)
        tax = '$' + str(round(float(purchaseOrderObj.taxRate) * total, 2))
        grandtotal = round(float(purchaseOrderObj.taxRate) * total, 2) + purchaseOrderObj.shipping - purchaseOrderObj.discount + total
        grandtotal = '$' + str(grandtotal)

        return render(request, 'reports/purchaseorder.html', {'purchaseOrder': purchaseOrderObj, 'purchaseOrderRowObj': purchaseOrderRowObj, 'subtotal': subtotal, 'tax': tax, 'shipping': shipping, 'discount': discount, 'grandtotal': grandtotal})