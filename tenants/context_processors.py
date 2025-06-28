from datetime import date
from django.conf import settings

current_year = date.today().year
company_name = settings.ORGANIZATION_NAME


def site_settings(request):
    return {
        "current_year": current_year,
        "company_name": company_name,
    }
