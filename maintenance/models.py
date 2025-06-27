import uuid
from django.db import models
from property.models import Property
from tenants.models import Tenant


class MaintenanceRequest(models.Model):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"

    MAINTENANCE_STATUS = (
        ("OPEN", "Open"),
        ("IN_PROGRESS", "In Progress"),
        ("CLOSED", "Closed"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=MAINTENANCE_STATUS, default=OPEN)
    created_at = models.DateTimeField(auto_now_add=True)
    is_delivered = models.BooleanField(default=False)

    class Meta:
        db_table = "maintenance"
        ordering = ["-created_at"]
        verbose_name = "Maintenance Request"
        verbose_name_plural = "Maintenance Requests"

    def __str__(self):
        return f"Maintenance for {self.property} - {self.status}"
