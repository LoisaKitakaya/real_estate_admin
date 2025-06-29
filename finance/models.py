import uuid
from django.db import models
from lease.models import Lease


class Payment(models.Model):
    PAID = "paid"
    PENDING = "pending"

    PAYMENT_STATUS = (
        (PAID, "Paid"),
        (PENDING, "Pending"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lease = models.ForeignKey(Lease, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "payment"
        ordering = ["-created_at"]
        verbose_name = "Payment"
        verbose_name_plural = "Payments"

    def __str__(self):
        return f"Payment for {self.lease} - {self.amount}"
