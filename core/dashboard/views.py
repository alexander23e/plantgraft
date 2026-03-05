import json
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, FloatField
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.views.generic import TemplateView

from core.erp.choices import TYPE_SALE, SALE_STATUS
from core.erp.models import Provider, Client, Resource, Product, Purchase, Sale
from core.security.models import Dashboard


class DashboardView(LoginRequiredMixin, TemplateView):
    def get_template_names(self):
        dashboard = Dashboard.objects.filter()
        if dashboard.exists():
            if dashboard[0].layout == 1:
                return 'vtc_dashboard.html'
        return 'hzt_dashboard.html'

    def get(self, request, *args, **kwargs):
        request.user.set_group_session()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'get_graph_stock_products':
                data = []
                for i in Product.objects.filter():
                    if i.stock > 0:
                        data.append({'name': i.name, 'y': i.stock})
            elif action == 'get_graph_stock_resources':
                data = []
                for i in Resource.objects.filter():
                    if i.stock > 0:
                        data.append([i.name, i.stock])
                data = sorted(data, key=lambda x: (-x[1]))[0:10]
            elif action == 'get_graph_purchases_sales':
                data = [
                    {'name': 'Compras', 'data': []},
                    {'name': 'Ventas', 'data': []},
                ]
                year = datetime.now().date().year
                queryset = Purchase.objects.filter(date_joined__year=year)
                for month in range(1, 13):
                    total = queryset.filter(date_joined__month=month).aggregate(result=Coalesce(Sum('subtotal'), 0.00, output_field=FloatField())).get('result')
                    data[0]['data'].append(round(float(total), 2))
                queryset = Sale.objects.filter(date_joined__year=year, paid=True).exclude(type=TYPE_SALE[1][0])
                for month in range(1, 13):
                    total = queryset.filter(date_joined__month=month).aggregate(result=Coalesce(Sum('total'), 0.00, output_field=FloatField())).get('result')
                    data[1]['data'].append(round(float(total), 2))
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Panel de administración'
        context['provider'] = Provider.objects.all().count()
        context['client'] = Client.objects.all().count()
        context['resource'] = Resource.objects.all().count()
        context['product'] = Product.objects.all().count()
        context['sales'] = Sale.objects.filter().order_by('-id')[0:10]
        return context