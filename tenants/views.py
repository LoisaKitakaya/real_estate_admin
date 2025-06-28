from django.contrib import messages
from django.shortcuts import render, redirect
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
