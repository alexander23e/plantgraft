import calendar
import json
import locale
import time

from django.db.models import Sum, FloatField
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.views.generic import FormView

from core.erp.choices import MONTHS
from core.erp.models import Sale, Client
from core.reports.forms import ReportForm
from core.security.mixins import ModuleMixin


class SalesControlBIView(ModuleMixin, FormView):
    template_name = 'sale_bi/sales_control.html'
    form_class = ReportForm

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'search_report':
                data = {'series': []}
                year = int(request.POST['year'])
                month = request.POST['month']
                locale.setlocale(locale.LC_ALL, '')
                categories = list(calendar.month_name)[1:]
                months = [m for m in range(1, 13)]
                if len(month):
                    month = int(month)
                    categories = [MONTHS[month][1]]
                    months = [month]
                queryset = Sale.objects.filter(date_joined__year=year, paid=True)
                for m in months:
                    total = float(queryset.filter(date_joined__month=int(m)).aggregate(result=Coalesce(Sum('total'), 0.00, output_field=FloatField())).get('result'))
                    data['series'].append(total)
                data['categories'] = categories
                data['total'] = round(float(sum(data['series'])), 2)
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        finally:
            time.sleep(1)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Dashboard de Control de Ventas'
        return context


class SalesPerCustomerBIView(ModuleMixin, FormView):
    template_name = 'sale_bi/sales_per_customer.html'
    form_class = ReportForm

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'search_report':
                data = []
                client_id = json.loads(request.POST['client'])
                if len(client_id):
                    year = int(request.POST['year'])
                    customers = Client.objects.filter()
                    customers = customers.filter(id__in=client_id)
                    for customer in customers:
                        item = {'name': customer.user.names, 'data': []}
                        queryset = Sale.objects.filter(date_joined__year=year, paid=True, client_id=customer.id)
                        for month, name in MONTHS[1:]:
                            total = float(queryset.filter(date_joined__month=int(month)).aggregate(result=Coalesce(Sum('total'), 0.00, output_field=FloatField())).get('result'))
                            item['data'].append(total)
                        data.append(item)
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        finally:
            time.sleep(1)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Dashboard de Ventas por Cliente'
        return context
