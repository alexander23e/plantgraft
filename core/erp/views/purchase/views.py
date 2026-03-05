import json

from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, FormView

from core.erp.forms import PurchaseForm, Purchase, PurchaseDetail, Resource, Provider, ProviderForm
from core.reports.forms import ReportForm
from core.security.mixins import PermissionMixin


class PurchaseListView(PermissionMixin, FormView):
    template_name = 'purchase/list.html'
    permission_required = 'view_purchase'
    form_class = ReportForm

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                queryset = Purchase.objects.filter()
                if len(start_date) and len(end_date):
                    queryset = queryset.filter(date_joined__range=[start_date, end_date])
                for i in queryset:
                    data.append(i.toJSON())
            elif action == 'search_detail_resources':
                data = []
                for i in PurchaseDetail.objects.filter(purchase_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('purchase_create')
        context['title'] = 'Listado de Compras'
        return context


class PurchaseCreateView(PermissionMixin, CreateView):
    model = Purchase
    template_name = 'purchase/create.html'
    form_class = PurchaseForm
    success_url = reverse_lazy('purchase_list')
    permission_required = 'add_purchase'

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'add':
                with transaction.atomic():
                    purchase = Purchase()
                    purchase.number = request.POST['number']
                    purchase.provider_id = int(request.POST['provider'])
                    purchase.date_joined = request.POST['date_joined']
                    purchase.save()

                    for i in json.loads(request.POST['resources']):
                        resource = Resource.objects.get(pk=i['id'])
                        purchasedetail = PurchaseDetail()
                        purchasedetail.purchase_id = purchase.id
                        purchasedetail.resource_id = resource.id
                        purchasedetail.cant = int(i['cant'])
                        purchasedetail.price = float(i['price'])
                        purchasedetail.subtotal = purchasedetail.cant * float(purchasedetail.price)
                        purchasedetail.save()

                        purchasedetail.resource.stock += purchasedetail.cant
                        purchasedetail.resource.save()

                    purchase.calculate_invoice()
            elif action == 'search_resources':
                data = []
                ids = json.loads(request.POST['ids'])
                term = request.POST['term']
                queryset = Resource.objects.filter().exclude(id__in=ids).order_by('name')
                if len(term):
                    queryset = queryset.filter(Q(name__icontains=term) | Q(code__icontains=term))
                    queryset = queryset[0:10]
                for i in queryset:
                    item = i.toJSON()
                    item['value'] = i.get_full_name()
                    data.append(item)
            elif action == 'search_provider':
                data = []
                for i in Provider.objects.filter(name__icontains=request.POST['term']).order_by('name')[0:10]:
                    item = i.toJSON()
                    item['text'] = i.get_full_name()
                    data.append(item)
            elif action == 'validate_provider':
                data = {'valid': True}
                queryset = Provider.objects.all()
                pattern = request.POST['pattern']
                parameter = request.POST['parameter'].strip()
                if pattern == 'name':
                    data['valid'] = not queryset.filter(name__iexact=parameter).exists()
                elif pattern == 'ruc':
                    data['valid'] = not queryset.filter(ruc=parameter).exists()
                elif pattern == 'mobile':
                    data['valid'] = not queryset.filter(mobile=parameter).exists()
                elif pattern == 'email':
                    data['valid'] = not queryset.filter(email=parameter).exists()
            elif action == 'validate_purchase':
                data = {'valid': True}
                pattern = request.POST['pattern']
                if pattern == 'number':
                    data['valid'] = not Purchase.objects.filter(number=request.POST['number']).exists()
            elif action == 'create_provider':
                form = ProviderForm(request.POST)
                data = form.save()
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['frmProvider'] = ProviderForm()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de una Compra'
        context['action'] = 'add'
        return context


class PurchaseDeleteView(PermissionMixin, DeleteView):
    model = Purchase
    template_name = 'purchase/delete.html'
    success_url = reverse_lazy('purchase_list')
    permission_required = 'delete_purchase'

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
