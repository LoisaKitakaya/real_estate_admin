import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

from lease.models import Lease
from tenants.models import Tenant


def create_customer(tenant: Tenant):
    customer = stripe.Customer.create(
        name=f"{tenant.user.first_name} {tenant.user.last_name}",
        email=f"{tenant.user.email}",
        phone=f"{tenant.phone}",
    )

    return customer.id


def update_customer(customer_id: str, tenant: Tenant):
    customer = stripe.Customer.modify(
        customer_id,
        name=f"{tenant.user.first_name} {tenant.user.last_name}",
        email=f"{tenant.user.email}",
        phone=f"{tenant.phone}",
    )

    return customer.id


def retrieve_customer(customer_id: str):
    customer = stripe.Customer.retrieve(customer_id)

    return customer


def delete_customer(customer_id: str):
    customer = stripe.Customer.delete(customer_id)

    return customer


def create_price(lease: Lease):
    price = stripe.Price.create(
        currency=settings.DEFAULT_CURRENCY,
        unit_amount=(int(lease.rent_amount) * 100),
        product_data={"name": f"{str(lease)}"},
    )

    return price.id


def update_price(price_id: str, lease: Lease):
    price = stripe.Price.modify(
        price_id,
        currency=settings.DEFAULT_CURRENCY,
        unit_amount=int(lease.rent_amount),
        product_data={"name": f"{str(lease)}"},
    )

    return price.id


def retrieve_price(price_id: str):
    price = stripe.Price.retrieve(price_id)

    return price


def create_payment_link(lease: Lease):
    payment_link = stripe.PaymentLink.create(
        line_items=[
            {
                "price": lease.stripe_price_id,
                "quantity": 1,
            }
        ],
        after_completion={
            "type": "redirect",
            "redirect": {"url": f"{settings.SITE_URL}/payments/success"},
        },
        metadata={
            "lease": str(lease),
            "lease_id": lease.id,
        },
    )

    return payment_link.url

def retrieve_payment_intent(intent_id: str):
    payment_intent = stripe.PaymentIntent.retrieve(intent_id)
    
    return payment_intent
