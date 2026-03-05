import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView

from core.erp.forms import Employee, EmployeeForm
from core.security.mixins import PermissionMixin


class EmployeeListView(PermissionMixin, TemplateView):
    template_name = 'employee/list.html'
    permission_required = 'view_employee'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in Employee.objects.filter():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('employee_create')
        context['title'] = 'Listado de Empleados'
        return context


class EmployeeCreateView(PermissionMixin, CreateView):
    model = Employee
    template_name = 'employee/create.html'
    form_class = EmployeeForm
    success_url = reverse_lazy('employee_list')
    permission_required = 'add_employee'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                data = self.get_form().save()
            elif action == 'validate_data':
                data = {'valid': True}
                pattern = request.POST['pattern']
                parameter = request.POST['parameter'].strip()
                queryset = Employee.objects.all()
                if pattern == 'dni':
                    data['valid'] = not queryset.filter(dni=parameter).exists()
                elif pattern == 'mobile':
                    data['valid'] = not queryset.filter(mobile=parameter).exists()
                elif pattern == 'email':
                    data['valid'] = not queryset.filter(email=parameter).exists()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de un Empleado'
        context['action'] = 'add'
        return context


class EmployeeUpdateView(PermissionMixin, UpdateView):
    model = Employee
    template_name = 'employee/create.html'
    form_class = EmployeeForm
    success_url = reverse_lazy('employee_list')
    permission_required = 'change_employee'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                data = self.get_form().save()
            elif action == 'validate_data':
                data = {'valid': True}
                pattern = request.POST['pattern']
                parameter = request.POST['parameter'].strip()
                queryset = Employee.objects.all().exclude(id=self.object.id)
                if pattern == 'dni':
                    data['valid'] = not queryset.filter(dni=parameter).exists()
                elif pattern == 'mobile':
                    data['valid'] = not queryset.filter(mobile=parameter).exists()
                elif pattern == 'email':
                    data['valid'] = not queryset.filter(email=parameter).exists()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de un Empleado'
        context['action'] = 'edit'
        return context


class EmployeeDeleteView(PermissionMixin, DeleteView):
    model = Employee
    template_name = 'employee/delete.html'
    success_url = reverse_lazy('employee_list')
    permission_required = 'delete_employee'

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
