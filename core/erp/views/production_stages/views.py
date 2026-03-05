import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView

from core.erp.forms import ProductionStagesForm
from core.erp.models import Production, ProductionStages
from core.security.mixins import PermissionMixin


class ProductionStagesCreateView(PermissionMixin, FormView):
    template_name = 'production_stages/create.html'
    form_class = ProductionStagesForm
    permission_required = 'view_production_stages'
    success_url = reverse_lazy('production_stages_create')

    def get_form(self, form_class=None):
        form = ProductionStagesForm()
        if 'pk' in self.kwargs:
            form.fields['production'].initial = self.kwargs['pk']
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                products = json.loads(request.POST['products'])
                for i in products:
                    production_stages = ProductionStages()
                    production_stages.production_products_id = int(i['id'])
                    production_stages.stage = production_stages.production_products.get_current_stage()
                    production_stages.observations = i['observations']
                    production_stages.save()
            elif action == 'search_production':
                production = Production.objects.get(pk=request.POST['id'])
                data = {'products': [], 'production': production.toJSON()}
                for i in production.productionproducts_set.all():
                    item = i.toJSON()
                    item['observations'] = ''
                    item['state'] = 0
                    item['current_stage'] = i.get_current_stage().toJSON()
                    data['products'].append(item)
            elif action == 'search_detail_stages':
                data = []
                for i in ProductionStages.objects.filter(production_products_id=request.POST['id']).order_by('stage_id'):
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registro de crecimiento de Plantas e Injertos'
        context['action'] = 'add'
        context['list_url'] = self.success_url
        return context
