"""garden URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views.main import Dashboard, Table, AddTable, ViewTable
from django.conf.urls.static import static
from django.conf import settings
from .tables import *
from .forms import *

urlpatterns = [
    path('', Dashboard.as_view()),
    path('assets/', include([
        path('', Table.as_view(tableObj=AssetTable), name='assets'),
        path('add/', AddTable.as_view(formObj=AssetForm)),
        path('view/<int:id>/', ViewTable.as_view(tableObj=AssetTable)),
    ])),
    path('config/organizations/', include([
        path('', Table.as_view(tableObj=OrganizationTable), name='organizations'),
        path('add/', AddTable.as_view(formObj=OrganizationForm)),
        path('view/<int:id>/', ViewTable.as_view(tableObj=OrganizationTable)),
    ])),
    path('config/departments/', include([
        path('', Table.as_view(tableObj=DepartmentTable), name='departments'),
        path('add/', AddTable.as_view(formObj=DepartmentForm)),
        path('view/<int:id>/', ViewTable.as_view(tableObj=DepartmentTable)),
    ])),
    path('config/manufacturers/', include([
        path('', Table.as_view(tableObj=ManufacturerTable), name='manufacturers'),
        path('add/', AddTable.as_view(formObj=ManufacturerForm)),
        path('view/<int:id>/', ViewTable.as_view(tableObj=ManufacturerTable)),
    ])),
    path('config/models/', include([
        path('', Table.as_view(tableObj=ModelTable), name='models'),
        path('add/', AddTable.as_view(formObj=ModelsForm)),
        path('view/<int:id>/', ViewTable.as_view(tableObj=ModelTable)),
    ])),
    path('admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
