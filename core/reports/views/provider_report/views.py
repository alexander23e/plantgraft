import json

from django.db.models import Q
from django.http import HttpResponse
from django.views.generic import FormView

from core.erp.models import Provider
from core.reports.forms import ReportForm
from core.security.mixins import ModuleMixin


class ProviderReportView(ModuleMixin, FormView):
    template_name = 'provider_report/report.html'
    form_class = ReportForm

    def get_form(self, form_class=None):
        form = ReportForm()
        form.fields['search'].widget.attrs.update({'placeholder': 'Ingrese un nombre o número de ruc'})
        return form

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'search_report':
                data = []
                term = request.POST['term']
                queryset = Provider.objects.filter()
                if len(term):
                    queryset = queryset.filter(Q(ruc__icontains=term) | Q(name__icontains=term))
                for i in queryset:
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Informe de Proveedores'
        return context
