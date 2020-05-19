"""garden URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, namespace='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), namespace='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views.main import Dashboard, Table, TableForm, DeleteTable, ViewTable, Logout, CheckoutFormView
from django.conf.urls.static import static
from django.conf import settings
from .tables import *
from .forms import *
from .views.api import AssetApiViewSet, ModelApiViewSet
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'assets', AssetApiViewSet)
router.register(r'models', ModelApiViewSet)

tablepatterns = ([
    path('', Table.as_view(), name="main"),
    path('add/', TableForm.as_view(), name="add"),
    path('delete/', DeleteTable.as_view(), name="delete"),
    path('view/<int:id>/', ViewTable.as_view(), name="view"),
    path('edit/<int:id>/', TableForm.as_view(), name="edit"),
], 'maintenance')

urlpatterns = [
    path('', Dashboard.as_view()),
    path('assets/', include(tablepatterns, namespace='asset'), {'tableObj': AssetTable}),
    path('components/', include(tablepatterns, namespace='component'), {'tableObj': ComponentTable}),
    path('purchasing/purchaseorders/', include(tablepatterns, namespace='purchaseorder'), {'tableObj': PurchaseOrderTable}),
    path('purchasing/purchaseorderrows/', include(tablepatterns, namespace='purchaseorderrow'), {'tableObj': PurchaseOrderRowTable}),
    path('maintenance/workorders/', include(tablepatterns, namespace='workorder'), {'tableObj': WorkOrderTable}),
    path('consumables/consumables/', include(tablepatterns, namespace='consumable'), {'tableObj': ConsumableTable}),
    path('consumables/consumableledger/', include(tablepatterns, namespace='consumableledger'), {'tableObj': ConsumableLedgerTable}),
    path('config/sites/', include(tablepatterns, namespace='site'), {'tableObj': SiteTable}),
    path('config/categories/', include(tablepatterns, namespace='category'), {'tableObj': CategoryTable}),
    path('config/departments/', include(tablepatterns, namespace='department'), {'tableObj': DepartmentTable}),
    path('config/manufacturers/', include(tablepatterns, namespace='manufacturer'), {'tableObj': ManufacturerTable}),
    path('config/models/', include(tablepatterns, namespace='model'), {'tableObj': ModelTable}),
    path('config/users/', include(tablepatterns, namespace='user'), {'tableObj': UserTable}),
    path('config/suppliers/', include(tablepatterns, namespace='supplier'), {'tableObj': SupplierTable}),
    path('config/addresses/', include(tablepatterns, namespace='address'), {'tableObj': AddressTable}),
    path('assets/checkoutform/', CheckoutFormView.as_view(), {'objForm': CheckoutForm}, name="checkoutform"),
    path('assets/checkinform/', CheckoutFormView.as_view(), {'objForm': CheckinForm}, name="checkinform"),
    path('login/', auth_views.LoginView.as_view()),
    path('logout/', Logout.as_view()),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

urlpatterns += staticfiles_urlpatterns()
