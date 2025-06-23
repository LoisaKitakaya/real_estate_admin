from django.db import models


class Property(models.Model):
    HOUSE = "house"
    APARTMENT = "apartment"
    COMMERCIAL = "commercial"

    PROPERTY_TYPES = (
        (HOUSE, "House"),
        (APARTMENT, "Apartment"),
        (COMMERCIAL, "Commercial"),
    )

    address = models.CharField(max_length=255)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    size = models.FloatField()
    is_occupied = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="properties/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "property"
        ordering = ["-created_at"]
        verbose_name = "Property"
        verbose_name_plural = "Properties"

    def __str__(self):
        return self.address
