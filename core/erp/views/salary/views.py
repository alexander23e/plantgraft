import json
import os

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, TemplateView
from weasyprint import HTML, CSS

from core.erp import printer
from core.erp.forms import *
from core.security.mixins import PermissionMixin


class SalaryListView(PermissionMixin, FormView):
    template_name = 'salary/list.html'
    permission_required = 'view_salary'
    form_class = SalaryForm

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'search':
                data = []
                year = request.POST['year']
                month = request.POST['month']
                search = Salary.objects.all()
                if len(year) and len(month):
                    search = search.filter(year=year, month=month)
                for i in search:
                    item = i.toJSON()
                    # item['days_work'] = i.contract.count_worked_days(year, month)
                    data.append(item)
            elif action == 'search_headings':
                data = []
                salary = Salary.objects.get(pk=request.POST['id'])
                for i in salary.salarydetail_set.filter(headings__type=request.POST['type']).filter(Q(valor__gt=0.00) | Q(total__gt=0.00)):
                    data.append(i.toJSON())
            elif action == 'search_assistance':
                data = []
                salary = Salary.objects.get(pk=request.POST['id'])
                for i in Assistance.objects.filter(employee_id=salary.employee_id, date_joined__year=salary.year, date_joined__month=salary.month):
                    data.append(i.toJSON())
            elif action == 'search_discounts':
                data = []
                salary = Salary.objects.get(pk=request.POST['id'])
                for i in salary.salarydetail_set.filter(headings__isnull=True):
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('salary_create')
        context['title'] = 'Listado de Roles de Pago'
        return context


class SalaryCreateView(PermissionMixin, FormView):
    template_name = 'salary/create.html'
    form_class = SalaryForm
    success_url = reverse_lazy('salary_list')
    permission_required = 'add_salary'

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'add':
                with transaction.atomic():
                    year = request.POST['year']
                    month = request.POST['month']
                    for i in json.loads(request.POST['salaries']):
                        salary = Salary()
                        salary.employee_id = int(i['id'])
                        salary.year = year
                        salary.month = month
                        salary.rmu_contract = float(i['rmu'])
                        salary.rmu_month = float(i['rmu_month'])
                        salary.salary_by_day = float(i['salary_by_day'])
                        salary.days_work = int(i['days_work'])
                        salary.egress = float(i['egress_total'])
                        salary.loan_discount = salary.employee.get_discount_loan()
                        salary.ingress = float(i['ingress_total'])
                        salary.save()
                        if salary.loan_discount > 0.00:
                            loan_payments = LoanPayments()
                            loan_payments.loans_id = Loans.objects.filter(employee_id=salary.employee_id, state=True)[0].id
                            loan_payments.salary_id = salary.id
                            loan_payments.valor = salary.loan_discount
                            loan_payments.save()
                        for d in i['ingress']:
                            detail = SalaryDetail()
                            detail.salary_id = salary.id
                            detail.headings_id = int(d['id'])
                            detail.valor = float(d['cant'])
                            detail.total = float(d['total'])
                            detail.save()
                        for d in i['egress']:
                            detail = SalaryDetail()
                            detail.salary_id = salary.id
                            detail.headings_id = int(d['id'])
                            detail.valor = float(d['cant'])
                            detail.total = float(d['total'])
                            detail.save()
                        total = float(salary.rmu_month) - float(salary.ingress) + float(salary.egress) - float(salary.loan_discount)
                        salary.total = total
                        salary.save()
            elif action == 'generate_salary':
                data = []
                year = request.POST['year']
                month = request.POST['month']
                for i in Employee.objects.filter(state=True):
                    item = i.toJSON()
                    salary_by_day = i.salary_by_day()
                    count_worked_days = i.count_worked_days(year, month)
                    rmu_month = float(salary_by_day) * count_worked_days
                    ingress = i.calculate_headings(type=TYPE_HEADINGS[0][0], rmu=rmu_month)
                    egress = i.calculate_headings(type=TYPE_HEADINGS[1][0], rmu=rmu_month)
                    loan_discount = i.get_discount_loan()
                    total = float(rmu_month) - float(ingress) - loan_discount + float(egress)
                    item['salary_by_day'] = float(salary_by_day)
                    item['days_work'] = count_worked_days
                    item['rmu_month'] = float(rmu_month)
                    item['ingress_total'] = float(ingress)
                    item['egress_total'] = float(egress)
                    item['loan_discount'] = loan_discount
                    item['total'] = float(total)
                    for type_heading in TYPE_HEADINGS:
                        headings = []
                        for h in i.headings.filter(type=type_heading[0]):
                            cant = 0.00
                            valor = 0.00
                            heading = h.toJSON()
                            if h.calculation_method == CALCULATION_METHOD[0][0]:
                                cant = float(h.valor)
                                valor = cant * rmu_month
                                heading['cant'] = float(rmu_month)
                            else:
                                heading['cant'] = float(cant)
                            heading['total'] = float(valor)
                            headings.append(heading)
                        item[type_heading[0]] = headings
                    data.append(item)
            elif action == 'search_assistance':
                data = []
                year = request.POST['year']
                month = request.POST['month']
                employee = request.POST['employee']
                for i in Assistance.objects.filter(employee_id=employee, date_joined__year=year, date_joined__month=month):
                    data.append(i.toJSON())
            elif action == 'validate_data':
                data = {'valid': True}
                year = request.POST['year']
                month = request.POST['month']
                if len(year) and len(month):
                    data['valid'] = not Salary.objects.filter(year=year, month=month).exists()
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de un Rol de Pago'
        context['action'] = 'add'
        return context


class SalaryUpdateView(PermissionMixin, FormView):
    template_name = 'salary/create.html'
    form_class = SalaryForm
    success_url = reverse_lazy('salary_list')
    permission_required = 'add_salary'

    def get(self, request, *args, **kwargs):
        year = self.kwargs['year']
        month = self.kwargs['month']
        if not Salary.objects.filter(year=year, month=month).exists():
            messages.error(request, f'El rol de pago del año {year} y del mes de {MONTHS[month][1]} no ha sido registrado')
            return HttpResponseRedirect(self.success_url)
        return super().get(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = SalaryForm(initial={
            'year_month': f"{self.kwargs['month']}/{self.kwargs['year']}"
        })
        form.fields['year_month'].widget.attrs.update({'disabled': True})
        return form

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'edit':
                with transaction.atomic():
                    year = request.POST['year']
                    month = request.POST['month']
                    Salary.objects.filter(year=year, month=month).delete()
                    for i in json.loads(request.POST['salaries']):
                        salary = Salary()
                        salary.employee_id = int(i['id'])
                        salary.year = year
                        salary.month = month
                        salary.rmu_contract = float(i['rmu'])
                        salary.rmu_month = float(i['rmu_month'])
                        salary.salary_by_day = float(i['salary_by_day'])
                        salary.days_work = int(i['days_work'])
                        salary.egress = float(i['egress_total'])
                        salary.ingress = float(i['ingress_total'])
                        salary.save()
                        for d in i['ingress']:
                            detail = SalaryDetail()
                            detail.salary_id = salary.id
                            detail.headings_id = int(d['id'])
                            detail.valor = float(d['cant'])
                            detail.total = float(d['total'])
                            detail.save()
                        for d in i['egress']:
                            detail = SalaryDetail()
                            detail.salary_id = salary.id
                            detail.headings_id = int(d['id'])
                            detail.valor = float(d['cant'])
                            detail.total = float(d['total'])
                            detail.save()
                        total = float(salary.rmu_month) + float(salary.ingress) - float(salary.egress)
                        salary.total = total
                        salary.save()
            elif action == 'generate_salary':
                data = []
                year = request.POST['year']
                month = request.POST['month']
                for i in Employee.objects.filter(state=True):
                    item = i.toJSON()
                    salary_by_day = i.salary_by_day()
                    count_worked_days = i.count_worked_days(year, month)
                    rmu_month = float(salary_by_day) * count_worked_days
                    ingress = i.calculate_headings_updated_salary(year=year, month=month, type=TYPE_HEADINGS[0][0], rmu=rmu_month)
                    egress = i.calculate_headings_updated_salary(year=year, month=month, type=TYPE_HEADINGS[1][0], rmu=rmu_month)
                    loan_discount = i.get_discount_loan()
                    total = float(rmu_month) - float(ingress) - loan_discount + float(egress)
                    item['salary_by_day'] = float(salary_by_day)
                    item['days_work'] = count_worked_days
                    item['rmu_month'] = float(rmu_month)
                    item['ingress_total'] = float(ingress)
                    item['egress_total'] = float(egress)
                    item['loan_discount'] = loan_discount
                    item['total'] = float(total)
                    salary_queryset = i.salary_set.filter(year=year, month=month)
                    if salary_queryset.exists():
                        salary = salary_queryset[0]
                        for type_heading in TYPE_HEADINGS:
                            headings = []
                            for h in salary.salarydetail_set.filter(headings__type=type_heading[0]):
                                heading = h.headings.toJSON()
                                heading['cant'] = float(h.valor)
                                heading['total'] = float(h.total)
                                headings.append(heading)
                            item[type_heading[0]] = headings
                    else:
                        for type_heading in TYPE_HEADINGS:
                            headings = []
                            for h in i.headings.filter(type=type_heading[0]):
                                cant = 0.00
                                valor = 0.00
                                heading = h.toJSON()
                                if h.calculation_method == CALCULATION_METHOD[0][0]:
                                    cant = float(h.valor)
                                    valor = cant * rmu_month
                                    heading['cant'] = float(rmu_month)
                                else:
                                    heading['cant'] = float(cant)
                                heading['total'] = float(valor)
                                headings.append(heading)
                            item[type_heading[0]] = headings
                    data.append(item)
            elif action == 'search_assistance':
                data = []
                year = request.POST['year']
                month = request.POST['month']
                employee = request.POST['employee']
                for i in Assistance.objects.filter(employee_id=employee, date_joined__year=year, date_joined__month=month):
                    data.append(i.toJSON())
            elif action == 'validate_data':
                data = {'valid': True}
                year = request.POST['year']
                month = request.POST['month']
                if len(year) and len(month):
                    data['valid'] = not Salary.objects.filter(year=year, month=month).exclude(year=year, month=month).exists()
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de un Rol de Pago'
        context['action'] = 'edit'
        return context


class SalaryDeleteView(PermissionMixin, TemplateView):
    template_name = 'salary/delete.html'
    success_url = reverse_lazy('salary_list')
    permission_required = 'delete_salary'

    def get(self, request, *args, **kwargs):
        year = self.kwargs['year']
        month = self.kwargs['month']
        if not Salary.objects.filter(year=year, month=month).exists():
            messages.error(request, f'El rol de pago del año {year} y del mes de {MONTHS[month][1]} no ha sido registrado')
            return HttpResponseRedirect(self.success_url)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            year = self.kwargs['year']
            month = self.kwargs['month']
            Salary.objects.filter(year=year, month=month).delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        context['year'] = self.kwargs['year']
        context['month'] = MONTHS[self.kwargs['month']][1]
        return context


class SalaryPrintReceiptView(LoginRequiredMixin, View):
    success_url = reverse_lazy('salary_list')

    def get_object(self):
        queryset = Salary.objects.filter(id=self.kwargs['pk'])
        if queryset.exists():
            return queryset[0]
        return None

    def get(self, request, *args, **kwargs):
        try:
            salary = self.get_object()
            if salary is not None:
                context = {
                    'salary': salary,
                    'company': Company.objects.first(),
                    'date_joined': datetime.now().date()
                }
                pdf_file = printer.create_pdf(context=context, template_name='salary/receipt.html')
                return HttpResponse(pdf_file, content_type='application/pdf')
        except:
            pass
        return HttpResponseRedirect(self.success_url)
