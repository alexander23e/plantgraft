import json
import time

from django.http import HttpResponse
from django.views.generic import FormView

from core.erp.models import Client
from core.reports.forms import ReportForm
from core.security.mixins import ModuleMixin


class CustomerRegisteredIView(ModuleMixin, FormView):
    template_name = 'client_bi/registered.html'
    form_class = ReportForm

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'search_report':
                data = []
                year = int(request.POST['year'])
                for month in range(1, 13):
                    count = Client.objects.filter(creation_date__year=year, creation_date__month=month).count()
                    data.append(count)
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        finally:
            time.sleep(1)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Dashboard de Clientes'
        return context
