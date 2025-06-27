from lease.models import Lease
from property.models import Property
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete


@receiver(post_save, sender=Lease)
def post_save_property(sender, instance, created, **kwargs):
    try:
        if created:
            property = Property.objects.get(id=instance.property.id)

            property.is_occupied = True

            property.save()
    except Exception as e:
        print(f"{str(e)}")


@receiver(post_delete, sender=Lease)
def post_delete_property(sender, instance, **kwargs):
    try:
        property = Property.objects.get(id=instance.property.id)

        property.is_occupied = False

        property.save()
    except Exception as e:
        print(f"{str(e)}")
