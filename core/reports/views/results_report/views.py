import json

from django.db.models import Sum, FloatField
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.views.generic import FormView

from core.erp.models import Purchase, Sale, Salary
from core.reports.forms import ReportForm
from core.security.mixins import ModuleMixin


class ResultsReportView(ModuleMixin, FormView):
    template_name = 'results_report/report.html'
    form_class = ReportForm

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'search_report':
                data = []
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                purchases = Purchase.objects.all()
                if len(start_date) and len(end_date):
                    purchases = purchases.filter(date_joined__range=[start_date, end_date])
                purchases = float(purchases.aggregate(result=Coalesce(Sum('subtotal'), 0.00, output_field=FloatField())).get('result'))
                sales = Sale.objects.all()
                if len(start_date) and len(end_date):
                    sales = sales.filter(date_joined__range=[start_date, end_date])
                sales = float(sales.aggregate(result=Coalesce(Sum('total'), 0.00, output_field=FloatField())).get('result'))
                salaries = Salary.objects.all()
                if len(start_date) and len(end_date):
                    salaries = salaries.filter(date_joined__range=[start_date, end_date])
                salaries = float(salaries.aggregate(result=Coalesce(Sum('total'), 0.00, output_field=FloatField())).get('result'))
                data.append(['Compras', purchases])
                data.append(['Ventas', sales])
                data.append(['Salarios', salaries])
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Informe de Resultados'
        return context
