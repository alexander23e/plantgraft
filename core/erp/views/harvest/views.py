import json

from django.db import transaction
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView

from core.erp.choices import STAGE_STATUS
from core.erp.forms import HarvestForm
from core.erp.models import Production, ProductionStages, ProductionProducts
from core.security.mixins import PermissionMixin


class HarvestCreateView(PermissionMixin, FormView):
    template_name = 'harvest/create.html'
    form_class = HarvestForm
    success_url = reverse_lazy('harvest_create')
    permission_required = 'view_harvest'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                with transaction.atomic():
                    products = json.loads(request.POST['products'])
                    date_joined = request.POST['date_joined']
                    for i in products:
                        production_products = ProductionProducts.objects.get(pk=i['id'])
                        production_products.status = STAGE_STATUS[-1][0]
                        production_products.loss = int(i['loss'])
                        production_products.harvest_date = date_joined
                        production_products.total = production_products.cant - production_products.loss
                        production_products.save()
                        production_products.product.stock += production_products.total
                        production_products.product.save()
            elif action == 'search_production':
                production = Production.objects.get(pk=request.POST['id'])
                data = {'products': [], 'production': production.toJSON()}
                for i in production.productionproducts_set.all():
                    item = i.toJSON()
                    item['current_stage'] = i.get_current_stage().toJSON()
                    item['state'] = 0
                    item['total'] = i.cant if i.total == 0 else i.total
                    data['products'].append(item)
            elif action == 'search_detail_stages':
                data = []
                for i in ProductionStages.objects.filter(production_products_id=request.POST['id']).order_by('stage_id'):
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de una Cosecha (Ingresos e Egresos)'
        context['action'] = 'add'
        return context
