import json

from django.http import HttpResponse
from django.views.generic import FormView

from core.erp.models import Production
from core.reports.forms import ReportForm
from core.security.mixins import ModuleMixin


class ProductionReportView(ModuleMixin, FormView):
    template_name = 'production_report/report.html'
    form_class = ReportForm

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'search_report':
                data = []
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                lot = request.POST['lot']
                queryset = Production.objects.filter()
                if len(lot):
                    queryset = queryset.filter(lot_id=lot)
                if len(start_date) and len(end_date):
                    queryset = queryset.filter(start_date__range=[start_date, end_date])
                for i in queryset:
                    item = i.toJSON()
                    item['resources'] = i.get_resources()
                    item['products'] = i.get_products()
                    data.append(item)
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Informe de Producciones'
        return context
