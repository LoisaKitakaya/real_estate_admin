from django.contrib import admin
from .models import Tenant
from lease.models import Lease
from maintenance.models import MaintenanceRequest
from communication.models import Message


class LeaseInline(admin.TabularInline):
    model = Lease
    extra = 1
    readonly_fields = ("created_at",)


class MaintenanceRequestInline(admin.TabularInline):
    model = MaintenanceRequest
    extra = 1
    readonly_fields = ("created_at",)


class MessageInline(admin.TabularInline):
    model = Message
    extra = 1
    readonly_fields = ("created_at",)


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = (
        "user__first_name",
        "user__last_name",
        "user__email",
        "phone",
        "created_at",
    )
    search_fields = ("user__first_name", "user__last_name", "user__email")
    inlines = [LeaseInline, MaintenanceRequestInline, MessageInline]
    readonly_fields = ("created_at",)
