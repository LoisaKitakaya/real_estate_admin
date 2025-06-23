from django.contrib import admin
from .models import MaintenanceRequest


@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ("property", "tenant", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("property__address", "tenant__email", "description")
    readonly_fields = ("created_at",)
