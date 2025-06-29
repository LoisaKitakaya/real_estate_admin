import uuid
from django.db import models
from users.models import User


class Tenant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tenants"
        ordering = ["-created_at"]
        verbose_name = "Tenant Profile"
        verbose_name_plural = "Tenant Profiles"

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
