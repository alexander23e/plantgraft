import json

from django.contrib import messages
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, FormView

from core.erp.forms import *
from core.security.mixins import PermissionMixin


class AssistanceListView(PermissionMixin, FormView):
    form_class = AssistanceForm
    template_name = 'assistance/list.html'
    permission_required = 'view_assistance'

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'search':
                data = []
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                queryset = Assistance.objects.all()
                if len(start_date) and len(end_date):
                    queryset = queryset.filter(date_joined__range=[start_date, end_date])
                for i in queryset:
                    data.append(i.toJSON())
            elif action == 'remove_assistance':
                assistance = Assistance.objects.get(pk=request.POST['id'])
                assistance.delete()
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('assistance_create')
        context['title'] = 'Listado de Asistencias'
        return context


class AssistanceCreateView(PermissionMixin, FormView):
    model = Assistance
    template_name = 'assistance/create.html'
    form_class = AssistanceForm
    success_url = reverse_lazy('assistance_list')
    permission_required = 'add_assistance'

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'add':
                with transaction.atomic():
                    date_joined = datetime.strptime(request.POST['date_joined'], '%Y-%m-%d')
                    for i in json.loads(request.POST['assistances']):
                        assistance = Assistance()
                        assistance.employee_id = int(i['id'])
                        assistance.date_joined = date_joined
                        assistance.details = i['details']
                        assistance.state = int(i['state']) == 1
                        assistance.save()
            elif action == 'validate_data':
                date_joined = request.POST['date_joined'].strip()
                data['valid'] = not Assistance.objects.filter(date_joined=date_joined).exists()
            elif action == 'generate_assistance':
                data = []
                curent_date = datetime.now()
                for i in Employee.objects.filter(state=True):
                    item = i.toJSON()
                    item['details'] = ''
                    item['state'] = 0
                    item['start_time'] = curent_date.strftime('%H:%M')
                    item['end_time'] = curent_date.strftime('%H:%M')
                    data.append(item)
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de una Asistencia'
        context['action'] = 'add'
        return context


class AssistanceUpdateView(PermissionMixin, CreateView):
    model = Assistance
    template_name = 'assistance/create.html'
    form_class = AssistanceForm
    success_url = reverse_lazy('assistance_list')
    permission_required = 'add_assistance'

    def get(self, request, *args, **kwargs):
        if not Assistance.objects.filter(date_joined=self.kwargs['date_joined']).exists():
            messages.error(request, f"La asistencia de la fecha {self.kwargs['date_joined']} aun no ha sido registrada")
            return HttpResponseRedirect(self.success_url)
        return super().get(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = AssistanceForm(initial={'date_joined': self.kwargs['date_joined']})
        form.fields['date_joined'].widget.attrs['disabled'] = True
        return form

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'edit':
                with transaction.atomic():
                    Assistance.objects.filter(date_joined=self.kwargs['date_joined']).delete()
                    date_joined = datetime.strptime(self.kwargs['date_joined'], '%Y-%m-%d')
                    for i in json.loads(request.POST['assistances']):
                        assistance = Assistance()
                        assistance.employee_id = int(i['id'])
                        assistance.date_joined = date_joined
                        assistance.details = i['details']
                        assistance.state = int(i['state']) == 1
                        assistance.save()
            elif action == 'validate_data':
                date_joined = request.POST['date_joined'].strip()
                data['valid'] = not Assistance.objects.filter(date_joined=date_joined).exclude(date_joined=date_joined).exists()
            elif action == 'generate_assistance':
                data = []
                for i in Employee.objects.filter(state=True):
                    item = i.toJSON()
                    item['state'] = 0
                    item['details'] = ''
                    assistance = i.assistance_set.filter(date_joined=self.kwargs['date_joined'])
                    if assistance.exists():
                        assistance = assistance[0]
                        item['state'] = 1 if assistance.state else 0
                        item['details'] = assistance.details
                    data.append(item)
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de un registro de una Asistencia'
        context['action'] = 'edit'
        return context


class AssistanceDeleteView(PermissionMixin, TemplateView):
    model = Assistance
    template_name = 'assistance/delete.html'
    success_url = reverse_lazy('assistance_list')
    permission_required = 'delete_assistance'

    def get(self, request, *args, **kwargs):
        start_date = self.kwargs['start_date']
        end_date = self.kwargs['end_date']
        if not Assistance.objects.filter(date_joined__range=[start_date, end_date]).exists():
            messages.error(request, f'La asistencia del día {start_date} al {end_date} aun no ha sido registrada')
            return HttpResponseRedirect(self.success_url)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            start_date = self.kwargs['start_date']
            end_date = self.kwargs['end_date']
            Assistance.objects.filter(date_joined__range=[start_date, end_date]).delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        context['dates'] = self.kwargs
        return context
