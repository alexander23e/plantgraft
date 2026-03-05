from datetime import datetime

from core.erp.models import Company
from core.homepage.models import SocialNetworks
from core.security.models import Dashboard


def system_information(request):
    dashboard = Dashboard.objects.first()
    parameters = {
        'dashboard': dashboard,
        'date_joined': datetime.now(),
        'company': Company.objects.first(),
        'social_networks': SocialNetworks.objects.filter(state=True),
        'menu': 'hzt_body.html' if dashboard is None else dashboard.get_template_from_layout()
    }
    return parameters
