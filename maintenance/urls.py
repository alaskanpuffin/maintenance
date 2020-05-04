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
from django.contrib.auth import views as auth_views
from .views.main import Dashboard, Table, TableForm, DeleteTable, ViewTable, Logout
from django.conf.urls.static import static
from django.conf import settings
from .tables import *
from .forms import *

urlpatterns = [
    path('', Dashboard.as_view()),
    path('assets/', include([
        path('', Table.as_view(tableObj=AssetTable), name='assets'),
        path('add/', TableForm.as_view(formObj=AssetForm)),
        path('delete/', DeleteTable.as_view(tableObj=AssetTable)),
        path('view/<int:id>/', ViewTable.as_view(tableObj=AssetTable)),
    ])),
    path('config/organizations/', include([
        path('', Table.as_view(tableObj=OrganizationTable), name='organization'),
        path('add/', TableForm.as_view(formObj=OrganizationForm)),
        path('delete/', DeleteTable.as_view(tableObj=OrganizationTable)),
        path('view/<int:id>/', ViewTable.as_view(tableObj=OrganizationTable)),
    ])),
    path('config/departments/', include([
        path('', Table.as_view(tableObj=DepartmentTable), name='department'),
        path('add/', TableForm.as_view(formObj=DepartmentForm)),
        path('delete/', DeleteTable.as_view(tableObj=DepartmentTable)),
        path('view/<int:id>/', ViewTable.as_view(tableObj=DepartmentTable)),
    ])),
    path('config/manufacturers/', include([
        path('', Table.as_view(tableObj=ManufacturerTable), name='manufacturer'),
        path('add/', TableForm.as_view(formObj=ManufacturerForm)),
        path('delete/', DeleteTable.as_view(tableObj=ManufacturerTable)),
        path('view/<int:id>/', ViewTable.as_view(tableObj=ManufacturerTable)),
    ])),
    path('config/models/', include([
        path('', Table.as_view(tableObj=ModelTable), name='model'),
        path('add/', TableForm.as_view(formObj=ModelsForm)),
        path('delete/', DeleteTable.as_view(tableObj=ModelTable)),
        path('view/<int:id>/', ViewTable.as_view(tableObj=ModelTable)),
    ])),
    path('login/', auth_views.LoginView.as_view()),
    path('logout/', Logout.as_view()),
    path('admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
