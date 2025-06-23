from django.contrib import admin
from .models import Property
from lease.models import Lease
from maintenance.models import MaintenanceRequest


class LeaseInline(admin.TabularInline):
    model = Lease
    extra = 1
    readonly_fields = ("created_at",)


class MaintenanceRequestInline(admin.TabularInline):
    model = MaintenanceRequest
    extra = 1
    readonly_fields = ("created_at",)


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ("address", "property_type", "size", "is_occupied", "created_at")
    list_filter = ("property_type", "is_occupied")
    search_fields = ("address", "description")
    inlines = [LeaseInline, MaintenanceRequestInline]
    readonly_fields = ("created_at", "updated_at")
