import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView, DeleteView

from core.erp.forms import LoansForm, Loans
from core.erp.models import LoanPayments
from core.reports.forms import ReportForm
from core.security.mixins import PermissionMixin


class LoansListView(PermissionMixin, FormView):
    template_name = 'loans/list.html'
    form_class = ReportForm
    permission_required = 'view_loans'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                queryset = Loans.objects.filter()
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                if len(start_date) and len(end_date):
                    queryset = queryset.filter(date_joined__range=[start_date, end_date])
                for i in queryset:
                    data.append(i.toJSON())
            elif action == 'search_detail_payments':
                data = []
                for i in LoanPayments.objects.filter(loans_id=request.POST['id']):
                    data.append(i.toJSON())
            elif action == 'delete_pay':
                LoanPayments.objects.get(pk=request.POST['id']).delete()
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('loans_create')
        context['title'] = 'Listado de Prestamos de Empleados'
        return context


class LoansCreateView(PermissionMixin, CreateView):
    model = Loans
    template_name = 'loans/create.html'
    form_class = LoansForm
    success_url = reverse_lazy('loans_list')
    permission_required = 'add_loans'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action', None)
        try:
            if action == 'add':
                data = self.get_form().save()
            elif action == 'validate_data':
                data = {'valid': True}
                queryset = Loans.objects.all()
                employee = request.POST['employee']
                if len(employee):
                    if queryset.filter(employee_id=employee, state=True).exists():
                        data = {'valid': False, 'message': f'El empleado ya cuenta un prestamo activo, para solicitar otro prestamo debe cancelar el prestamo actual y la deuda que es de ${queryset[0].saldo}'}
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de un Prestamo'
        context['action'] = 'add'
        return context


class LoansDeleteView(PermissionMixin, DeleteView):
    model = Loans
    template_name = 'loans/delete.html'
    success_url = reverse_lazy('loans_list')
    permission_required = 'delete_loans'

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
