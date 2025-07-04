from tenants import views
from django.urls import path

urlpatterns = [
    path("", views.home, name="home"),
    path("login", views.sign_in, name="login"),
    path("logout", views.sign_out, name="logout"),
    path("profile", views.profile, name="profile"),
    path("payments", views.payments, name="payments"),
    path("payments/make_payment", views.make_payment, name="make_payment"),
    path("payments/stripe_webhook", views.stripe_webhook, name="webhook"),
    path("payments/success", views.success, name="success"),
    path("maintenance", views.maintenance, name="maintenance"),
]
