import json

from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView, DeleteView

from core.erp.forms import Production, ProductionForm, Resource, ProductionResources, ProductionProducts
from core.erp.models import Product
from core.reports.forms import ReportForm
from core.security.mixins import PermissionMixin


class ProductionListView(PermissionMixin, FormView):
    template_name = 'production/list.html'
    form_class = ReportForm
    permission_required = 'view_production'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                queryset = Production.objects.filter()
                if len(start_date) and len(end_date):
                    queryset = queryset.filter(start_date__range=[start_date, end_date])
                for i in queryset:
                    data.append(i.toJSON())
            elif action == 'search_detail_resources':
                data = []
                for i in ProductionResources.objects.filter(production_id=request.POST['id']):
                    data.append(i.toJSON())
            elif action == 'search_detail_products':
                data = []
                production = Production.objects.get(pk=request.POST['id'])
                for i in production.productionproducts_set.filter(production_id=production.id):
                    data.append(i.toJSON())
            elif action == 'finish_production':
                production = Production.objects.get(pk=request.POST['id'])
                production.state = False
                production.save()
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('production_create')
        context['title'] = 'Listado de Producciones'
        return context


class ProductionCreateView(PermissionMixin, CreateView):
    model = Production
    template_name = 'production/create.html'
    form_class = ProductionForm
    success_url = reverse_lazy('production_list')
    permission_required = 'add_production'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                with transaction.atomic():
                    production = Production()
                    production.start_date = request.POST['date_joined']
                    production.lot_id = int(request.POST['lot'])
                    production.save()
                    for i in json.loads(request.POST['resources']):
                        resource = Resource.objects.get(pk=i['id'])
                        detail = ProductionResources()
                        detail.production_id = production.id
                        detail.resource_id = resource.id
                        detail.cant = int(i['cant'])
                        detail.price = float(i['price'])
                        detail.subtotal = detail.cant * float(detail.price)
                        detail.save()
                        detail.resource.stock -= detail.cant
                        detail.resource.save()
                    for i in json.loads(request.POST['products']):
                        detail = ProductionProducts()
                        detail.production_id = production.id
                        detail.product_id = int(i['id'])
                        detail.cant = int(i['cant'])
                        detail.save()
            elif action == 'search_resources':
                data = []
                ids = json.loads(request.POST['ids'])
                term = request.POST['term']
                queryset = Resource.objects.filter(stock__gt=0).exclude(id__in=ids).order_by('name')
                if len(term):
                    queryset = queryset.filter(Q(name__icontains=term) | Q(code__icontains=term))
                    queryset = queryset[0:10]
                for i in queryset:
                    item = i.toJSON()
                    item['value'] = i.get_full_name()
                    data.append(item)
            elif action == 'search_products':
                data = []
                ids = json.loads(request.POST['ids'])
                term = request.POST['term']
                queryset = Product.objects.filter().exclude(id__in=ids).order_by('name')
                if len(term):
                    queryset = queryset.filter(name__icontains=term)
                    queryset = queryset[0:10]
                for i in queryset:
                    item = i.toJSON()
                    item['value'] = i.get_full_name()
                    data.append(item)
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de una Producción'
        context['action'] = 'add'
        return context


class ProductionDeleteView(PermissionMixin, DeleteView):
    model = Production
    template_name = 'production/delete.html'
    success_url = reverse_lazy('production_list')
    permission_required = 'delete_production'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.get_object().delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        return context
