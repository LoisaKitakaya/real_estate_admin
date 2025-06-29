from lease.models import Lease
from tenants.models import Tenant
from django.contrib import messages
from property.models import Property
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


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
