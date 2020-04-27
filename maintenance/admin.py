from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from django.contrib import admin

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    pass

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    pass

@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    pass

@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    pass

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    pass

admin.site.register(CustomUser, UserAdmin)
