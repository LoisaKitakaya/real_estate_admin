import uuid
import stripe
import logging
from lease.models import Lease
from django.conf import settings
from tenants.models import Tenant
from finance.models import Payment
from django.contrib import messages
from property.models import Property
from datetime import timedelta, date
from django.shortcuts import render, redirect
from maintenance.models import MaintenanceRequest
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_http_methods
from utils.stripe import create_payment_link, retrieve_payment_intent


logger = logging.getLogger(__name__)
stripe.api_key = settings.STRIPE_SECRET_KEY


def home(request):
    context = {}

    return render(request, "tenants/home.html", context)


def sign_in(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)

            messages.success(request, "Successfully authenticated credentials")

            return redirect("home")
        else:
            messages.error(request, "Invalid username or password")

    context = {}

    return render(request, "auth/login.html", context)


def sign_out(request):
    logout(request)

    return redirect("login")


@login_required(login_url="/login")
def profile(request):
    current_user = request.user

    tenant = Tenant.objects.get(user=current_user)

    lease = Lease.objects.get(tenant=tenant)

    property = Property.objects.get(id=lease.property.id)

    context = {
        "tenant_info": {
            "tenant_id": str(tenant.pk),
            "username": current_user.username,
            "email": current_user.email,
            "first_name": current_user.first_name,
            "last_name": current_user.last_name,
            "phone": tenant.phone,
        },
        "lease_info": {
            "property_id": str(property.pk),
            "address": property.address,
            "property_type": property.property_type,
            "size": f"{property.size} Square Feet",
            "description": property.description,
            "image": property.image.url,
            "lease_id": str(lease.pk),
            "lease_start_date": lease.start_date,
            "lease_end_date": lease.end_date,
            "rent_amount": lease.rent_amount,
        },
    }

    return render(request, "tenants/profile.html", context)


@login_required(login_url="/login")
def payments(request):
    current_user = request.user

    tenant = Tenant.objects.get(user=current_user)

    lease = Lease.objects.get(tenant=tenant)

    payments = Payment.objects.filter(lease=lease)

    context = {
        "lease": lease,
        "payments": payments,
    }

    return render(request, "tenants/payments.html", context)


@login_required(login_url="/login")
def maintenance(request):
    current_user = request.user

    tenant = Tenant.objects.get(user=current_user)

    if request.method == "POST":
        description = request.POST.get("description")

        lease = Lease.objects.get(tenant=tenant)

        MaintenanceRequest.objects.create(
            property=lease.property,
            tenant=tenant,
            description=description,
        )

    context = {
        "maintenance_requests": MaintenanceRequest.objects.filter(tenant=tenant),
    }

    return render(request, "tenants/maintenance.html", context)


@login_required(login_url="/login")
@require_http_methods(["POST"])
def make_payment(request):
    current_user = request.user

    tenant = Tenant.objects.get(user=current_user)

    lease = Lease.objects.get(tenant=tenant)

    url = create_payment_link(lease)

    return redirect(url)


def success(request):
    return render(request, "components/success.html")


@csrf_exempt
@require_http_methods(["POST"])
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]

    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return JsonResponse({"status": "invalid payload"}, status=400)
    except stripe.error.SignatureVerificationError:
        return JsonResponse({"status": "invalid signature"}, status=400)

    if event["type"] == "checkout.session.completed":
        checkout_session = event["data"]["object"]

        print(f"Payment was successful! Checkout session object: {checkout_session}")

        try:
            assert checkout_session["payment_status"] == "paid"
        except Exception as e:
            print(f"Payment not completed: {str(e)}")

            return JsonResponse({"status": "failed"}, status=400)

        lease = Lease.objects.get(
            id=uuid.UUID(checkout_session["metadata"]["lease_id"])
        )

        payment = Payment.objects.create(
            lease=lease,
            amount=(int(checkout_session["amount_total"]) / 100),
            payment_date=date.today(),
        )

        payment.status = "paid"

        payment.save()

        previous_deadline = lease.end_date

        next_deadline = previous_deadline + timedelta(days=30)

        lease.start_date = previous_deadline

        lease.end_date = next_deadline

        lease.save()

    return JsonResponse({"status": "success"}, status=200)
