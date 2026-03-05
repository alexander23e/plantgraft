import json
import time

from django.db.models import Sum, IntegerField
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.views.generic import FormView

from core.erp.choices import PRODUCT_OPTIONS
from core.erp.models import SaleDetail, Product
from core.reports.forms import ReportForm
from core.security.mixins import ModuleMixin


class ProductInquiriesBIView(ModuleMixin, FormView):
    template_name = 'product_bi/product_inquiries.html'
    form_class = ReportForm

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'search_report':
                data = []
                option = request.POST['option']
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                queryset = SaleDetail.objects.filter()
                if len(start_date) and len(end_date):
                    queryset = queryset.filter(sale__date_joined__range=[start_date, end_date])
                products_id_sale = list(queryset.order_by('product_id').distinct().values_list('product_id', flat=True))
                for i in Product.objects.filter(id__in=products_id_sale):
                    total = i.saledetail_set.filter().aggregate(result=Coalesce(Sum('cant'), 0, output_field=IntegerField())).get('result')
                    data.append({'name': i.name, 'y': total})
                if option == PRODUCT_OPTIONS[0][0]:
                    data = sorted(data, key=lambda x: -x['y'])
                else:
                    data = sorted(data, key=lambda x: x['y'])
                data = data[0:10]
                if len(data):
                    data[0]['sliced'] = True
                    data[0]['selected'] = True
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        finally:
            time.sleep(1)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Dashboard de Productos'
        return context


class ProductsInventoryBIView(ModuleMixin, FormView):
    template_name = 'product_bi/products_inventory.html'
    form_class = ReportForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if Product.objects.filter().exists():
            form.fields['product'].initial = Product.objects.first().id
        return form

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'search_report':
                data = []
                year = int(request.POST['year'])
                product_id = request.POST['product']
                if len(product_id):
                    product = Product.objects.get(pk=product_id)
                    item = {'name': 'Cosecha', 'data': []}
                    for month in range(1, 13):
                        count = product.productionproducts_set.filter(harvest_date__year=year, harvest_date__month=month).aggregate(result=Coalesce(Sum('total'), 0, output_field=IntegerField())).get('result')
                        item['data'].append(count)
                    data.append(item)
                    item = {'name': 'Ventas', 'data': []}
                    for month in range(1, 13):
                        count = product.saledetail_set.filter(sale__date_joined__year=year, sale__date_joined__month=month).aggregate(result=Coalesce(Sum('cant'), 0, output_field=IntegerField())).get('result')
                        item['data'].append(count)
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
        context['title'] = 'Dashboard de Ingreso y Salida de Producto'
        return context


class ProductsPricesBIView(ModuleMixin, FormView):
    template_name = 'product_bi/products_prices.html'
    form_class = ReportForm

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'search_report':
                categories = [i.name for i in Product.objects.filter().order_by('id')]
                series = [float(i.price) for i in Product.objects.filter().order_by('id')]
                data['categories'] = categories
                data['series'] = series
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        finally:
            time.sleep(1)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Dashboard de Precios de Productos'
        return context
