from django.contrib import admin
from .models import Lease
from finance.models import Payment


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 1
    readonly_fields = ("created_at",)


@admin.register(Lease)
class LeaseAdmin(admin.ModelAdmin):
    list_display = (
        "property",
        "tenant",
        "start_date",
        "end_date",
        "rent_amount",
        "created_at",
    )
    list_filter = ("start_date", "end_date")
    search_fields = ("property__address", "tenant__email")
    inlines = [PaymentInline]
    readonly_fields = ("created_at",)
