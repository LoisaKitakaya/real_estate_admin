from tenants import views
from django.urls import path

urlpatterns = [
    path("", views.home, name="home"),
    path("login", views.sign_in, name="login"),
    path("logout", views.sign_out, name="logout"),
]
