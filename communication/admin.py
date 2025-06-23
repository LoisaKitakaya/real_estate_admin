from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "sender", "recipient", "is_delivered", "created_at")
    list_filter = ("is_delivered",)
    search_fields = ("subject", "body", "recipient__email")
    readonly_fields = ("created_at",)
