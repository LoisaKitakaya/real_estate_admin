from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("lease", "amount", "payment_date", "status", "created_at")
    list_filter = ("status", "payment_date")
    search_fields = ("lease__property__address", "lease__tenant__email")
    readonly_fields = ("created_at",)
