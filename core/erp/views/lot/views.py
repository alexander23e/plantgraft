import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.forms import Lot, LotForm
from core.security.mixins import PermissionMixin


class LotListView(PermissionMixin, ListView):
    model = Lot
    template_name = 'lot/list.html'
    permission_required = 'view_lot'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('lot_create')
        context['title'] = 'Listado de Lotes'
        return context


class LotCreateView(PermissionMixin, CreateView):
    model = Lot
    template_name = 'lot/create.html'
    form_class = LotForm
    success_url = reverse_lazy('lot_list')
    permission_required = 'add_lot'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                data = self.get_form().save()
            elif action == 'validate_data':
                data = {'valid': True}
                queryset = Lot.objects.all()
                pattern = request.POST['pattern']
                parameter = request.POST['parameter'].strip()
                if pattern == 'code':
                    data['valid'] = not queryset.filter(code__iexact=parameter).exists()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de un Lote'
        context['action'] = 'add'
        return context


class LotUpdateView(PermissionMixin, UpdateView):
    model = Lot
    template_name = 'lot/create.html'
    form_class = LotForm
    success_url = reverse_lazy('lot_list')
    permission_required = 'change_lot'

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
                queryset = Lot.objects.all().exclude(id=self.object.id)
                pattern = request.POST['pattern']
                parameter = request.POST['parameter'].strip()
                if pattern == 'code':
                    data['valid'] = not queryset.filter(code__iexact=parameter).exists()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de un Lote'
        context['action'] = 'edit'
        return context


class LotDeleteView(PermissionMixin, DeleteView):
    model = Lot
    template_name = 'lot/delete.html'
    success_url = reverse_lazy('lot_list')
    permission_required = 'delete_lot'

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
