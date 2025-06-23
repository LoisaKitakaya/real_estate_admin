from django.db import models
from property.models import Property
from tenants.models import Tenant


class Lease(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    document = models.FileField(upload_to="leases/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "lease"
        ordering = ["-created_at"]
        verbose_name = "Lease"
        verbose_name_plural = "Leases"

    def __str__(self):
        return f"Lease for {self.property} - {self.tenant}"
