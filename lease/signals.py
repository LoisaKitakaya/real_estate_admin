from lease.models import Lease
from finance.models import Payment
from property.models import Property
from datetime import date, timedelta
from django.dispatch import receiver
from utils.stripe import create_price
from django.db.models.signals import post_save, post_delete


@receiver(post_save, sender=Lease)
def post_save_property(sender, instance, created, **kwargs):
    try:
        if created:
            lease = Lease.objects.get(id=instance.id)
            
            lease.stripe_price_id = create_price(lease)
            
            lease.save()
            
            property = Property.objects.get(id=instance.property.id)

            property.is_occupied = True

            property.save()
    except Exception as e:
        raise str(e)


@receiver(post_delete, sender=Lease)
def post_delete_property(sender, instance, **kwargs):
    try:
        property = Property.objects.get(id=instance.property.id)

        property.is_occupied = False

        property.save()
    except Exception as e:
        raise str(e)

@receiver(post_save, sender=Payment)
def post_save_payment(sender, instance, created, **kwargs):
    try:
        if created:
            lease = Lease.objects.get(id=instance.lease.id)
            
            previous_deadline = lease.end_date
            
            next_deadline = previous_deadline + timedelta(days=30)
            
            lease.start_date = previous_deadline
            
            lease.end_date = next_deadline
            
            lease.save()
    except Exception as e:
        raise str(e)