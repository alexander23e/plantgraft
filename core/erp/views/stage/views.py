import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView

from core.erp.forms import Stage, StageForm
from core.security.mixins import PermissionMixin


class StageListView(PermissionMixin, TemplateView):
    template_name = 'stage/list.html'
    permission_required = 'view_stage'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                queryset = Stage.objects.filter()
                for i in queryset:
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('stage_create')
        context['title'] = 'Listado de Etapas de Cosecha'
        return context


class StageCreateView(PermissionMixin, CreateView):
    model = Stage
    template_name = 'stage/create.html'
    form_class = StageForm
    success_url = reverse_lazy('stage_list')
    permission_required = 'add_stage'

    def get_form(self, form_class=None):
        form = super(StageCreateView, self).get_form(form_class)
        form.fields['color'].initial = '#000000'
        form.fields['step'].initial = Stage.objects.count() + 1
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                data = self.get_form().save()
            elif action == 'validate_data':
                data = {'valid': True}
                queryset = Stage.objects.all()
                pattern = request.POST['pattern']
                parameter = request.POST['parameter'].strip()
                if pattern == 'step':
                    data['valid'] = not queryset.filter(step__iexact=parameter).exists()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de una Etapa de Cosecha'
        context['action'] = 'add'
        return context


class StageUpdateView(PermissionMixin, UpdateView):
    model = Stage
    template_name = 'stage/create.html'
    form_class = StageForm
    success_url = reverse_lazy('stage_list')
    permission_required = 'change_stage'

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
                queryset = Stage.objects.all().exclude(id=self.object.id)
                pattern = request.POST['pattern']
                parameter = request.POST['parameter'].strip()
                if pattern == 'step':
                    data['valid'] = not queryset.filter(step__iexact=parameter).exists()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de una Etapa de Cosecha'
        context['action'] = 'edit'
        return context


class StageDeleteView(PermissionMixin, DeleteView):
    model = Stage
    template_name = 'stage/delete.html'
    success_url = reverse_lazy('stage_list')
    permission_required = 'delete_stage'

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
