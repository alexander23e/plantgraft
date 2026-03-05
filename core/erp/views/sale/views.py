import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, FormView

from core.erp import printer
from core.erp.forms import *
from core.reports.forms import ReportForm
from core.security.mixins import PermissionMixin


class SaleListView(PermissionMixin, FormView):
    template_name = 'sale/admin/list.html'
    form_class = ReportForm
    permission_required = 'view_sale'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                queryset = Sale.objects.filter()
                if len(start_date) and len(end_date):
                    queryset = queryset.filter(date_joined__range=[start_date, end_date])
                for i in queryset:
                    data.append(i.toJSON())
            elif action == 'search_detail_products':
                data = []
                for i in SaleDetail.objects.filter(sale_id=request.POST['id']):
                    data.append(i.toJSON())
            elif action == 'upload_voucher':
                sale = Sale.objects.get(pk=request.POST['id'])
                sale.voucher = request.FILES['voucher']
                sale.save()
                sale.dispatch_products()
            elif action == 'check_available_stock_of_products':
                sale = Sale.objects.get(pk=request.POST['id'])
                data = sale.check_available_stock_of_products()
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('sale_admin_create')
        context['title'] = 'Listado de Ventas'
        context['frmSale'] = SaleForm()
        return context


class SaleCreateView(PermissionMixin, CreateView):
    model = Sale
    template_name = 'sale/admin/create.html'
    form_class = SaleForm
    success_url = reverse_lazy('sale_admin_list')
    permission_required = 'add_sale'

    def get_form(self, form_class=None):
        form = SaleForm()
        client = Client.objects.filter(user__dni='9999999999')
        if client.exists():
            client = client[0]
            form.fields['client'].queryset = Client.objects.filter(id=client.id)
            form.initial = {'client': client}
        return form

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'add':
                with transaction.atomic():
                    iva = float(Company.objects.first().iva) / 100
                    sale = Sale()
                    sale.date_joined = request.POST['date_joined']
                    sale.employee_id = request.user.id
                    sale.client_id = int(request.POST['client'])
                    sale.type = request.POST['type']
                    sale.paid = sale.type == TYPE_SALE[0][0]
                    sale.set_status()
                    sale.iva = iva
                    sale.save()
                    for i in json.loads(request.POST['products']):
                        product = Product.objects.get(pk=i['id'])
                        detail = SaleDetail()
                        detail.sale_id = sale.id
                        detail.product_id = product.id
                        detail.cant = int(i['cant'])
                        detail.price = float(i['price_current'])
                        detail.save()
                        if sale.type == TYPE_SALE[0][0]:
                            detail.product.stock -= detail.cant
                            detail.product.save()
                    sale.calculate_invoice()
                    sale.number = sale.generate_invoice_number()
                    sale.save()
                    print_url = reverse_lazy('sale_admin_print_invoice', kwargs={'pk': sale.id})
                    data = {'print_url': str(print_url)}
            elif action == 'search_products':
                ids = json.loads(request.POST['ids'])
                data = []
                term = request.POST['term']
                queryset = Product.objects.filter(stock__gt=0).exclude(id__in=ids).order_by('name')
                if len(term):
                    queryset = queryset.filter(Q(name__icontains=term) | Q(code__icontains=term))
                    queryset = queryset[:10]
                for i in queryset:
                    item = i.toJSON()
                    item['value'] = i.get_full_name()
                    data.append(item)
            elif action == 'search_client':
                data = []
                term = request.POST['term']
                for i in Client.objects.filter(Q(user__names__icontains=term) | Q(user__dni__icontains=term)).order_by('user__names')[0:10]:
                    item = i.toJSON()
                    item['text'] = i.get_full_name()
                    data.append(item)
            elif action == 'validate_client':
                data = {'valid': True}
                pattern = request.POST['pattern']
                parameter = request.POST['parameter'].strip()
                queryset = Client.objects.all()
                if pattern == 'dni':
                    data['valid'] = not queryset.filter(user__dni=parameter).exists()
                elif pattern == 'mobile':
                    data['valid'] = not queryset.filter(mobile=parameter).exists()
                elif pattern == 'email':
                    if len(parameter):
                        data['valid'] = not queryset.filter(user__email=parameter).exists()
            elif action == 'create_client':
                with transaction.atomic():
                    form1 = ClientUserForm(self.request.POST, self.request.FILES)
                    form2 = ClientForm(request.POST)
                    if form1.is_valid() and form2.is_valid():
                        user = form1.save(commit=False)
                        user.username = form1.cleaned_data.get('dni')
                        user.set_password(user.dni)
                        user.save()
                        user.groups.add(Group.objects.get(pk=settings.GROUPS.get('client')))
                        form_client = form2.save(commit=False)
                        form_client.user = user
                        form_client.save()
                        data = Client.objects.get(pk=form_client.id).toJSON()
                    else:
                        if not form1.is_valid():
                            data['error'] = form1.errors
                        elif not form2.is_valid():
                            data['error'] = form2.errors
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['frmClient'] = ClientForm()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de una Venta'
        context['action'] = 'add'
        context['frmUser'] = ClientUserForm()
        return context


class SaleDeleteView(PermissionMixin, DeleteView):
    model = Sale
    template_name = 'sale/admin/delete.html'
    success_url = reverse_lazy('sale_admin_list')
    permission_required = 'delete_sale'

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


class SalePrintInvoiceView(LoginRequiredMixin, View):
    success_url = reverse_lazy('sale_admin_list')

    def get_success_url(self):
        if self.request.user.is_client():
            return reverse_lazy('sale_client_list')
        return self.success_url

    def get_object(self):
        queryset = Sale.objects.filter(id=self.kwargs['pk'])
        if queryset.exists():
            return queryset[0]
        return None

    def get(self, request, *args, **kwargs):
        try:
            sale = self.get_object()
            if sale is not None:
                context = {'sale': sale, 'company': Company.objects.first(), 'height': 450 + sale.saledetail_set.all().count() * 10}
                pdf_file = printer.create_pdf(context=context, template_name='sale/format/ticket.html')
                return HttpResponse(pdf_file, content_type='application/pdf')
        except:
            pass
        return HttpResponseRedirect(self.get_success_url())


class SaleClientListView(PermissionMixin, FormView):
    template_name = 'sale/client/list.html'
    form_class = ReportForm
    permission_required = 'view_sale_client'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                queryset = Sale.objects.filter(client__user_id=request.user.id)
                if len(start_date) and len(end_date):
                    queryset = queryset.filter(date_joined__range=[start_date, end_date])
                for i in queryset:
                    data.append(i.toJSON())
            elif action == 'search_detail_products':
                data = []
                for i in SaleDetail.objects.filter(sale_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Ventas'
        context['create_url'] = reverse_lazy('sale_client_create')
        return context


class SaleClientCreateView(PermissionMixin, CreateView):
    model = Sale
    template_name = 'sale/client/create.html'
    form_class = SaleForm
    success_url = reverse_lazy('sale_client_list')
    permission_required = 'add_sale_client'

    def get_form(self, form_class=None):
        form = super(SaleClientCreateView, self).get_form(form_class)
        form.fields['type'].choices = tuple([value for count, value in enumerate(TYPE_SALE) if value[0] != TYPE_SALE[0][0]])
        form.fields['customer_names'].initial = self.request.user.names
        form.fields['customer_dni'].initial = self.request.user.dni
        return form

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'add':
                with transaction.atomic():
                    iva = float(Company.objects.first().iva) / 100
                    sale = Sale()
                    sale.date_joined = request.POST['date_joined']
                    sale.employee_id = request.user.id
                    sale.client_id = request.user.client.id
                    sale.type = request.POST['type']
                    sale.paid = sale.type == TYPE_SALE[0][0]
                    sale.set_status()
                    sale.iva = iva
                    sale.save()
                    for i in json.loads(request.POST['products']):
                        product = Product.objects.get(pk=i['id'])
                        detail = SaleDetail()
                        detail.sale_id = sale.id
                        detail.product_id = product.id
                        detail.cant = int(i['cant'])
                        detail.price = float(i['price_current'])
                        detail.save()
                        if sale.type == TYPE_SALE[0][0]:
                            detail.product.stock -= detail.cant
                            detail.product.save()
                    sale.calculate_invoice()
                    sale.number = sale.generate_invoice_number()
                    sale.save()
                    print_url = reverse_lazy('sale_admin_print_invoice', kwargs={'pk': sale.id})
                    data = {'print_url': str(print_url)}
            elif action == 'search_products':
                ids = json.loads(request.POST['ids'])
                data = []
                term = request.POST['term']
                queryset = Product.objects.filter(stock__gt=0).exclude(id__in=ids).order_by('name')
                if len(term):
                    queryset = queryset.filter(Q(name__icontains=term) | Q(code__icontains=term))
                    queryset = queryset[:10]
                for i in queryset:
                    item = i.toJSON()
                    item['value'] = i.get_full_name()
                    data.append(item)
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de una Venta'
        context['action'] = 'add'
        return context