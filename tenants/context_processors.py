from datetime import date
from django.conf import settings

current_year = date.today().year
company_name = settings.ORGANIZATION_NAME
default_currency = settings.DEFAULT_CURRENCY


def site_settings(request):
    return {
        "current_year": current_year,
        "company_name": company_name,
        "default_currency": default_currency,
    }
