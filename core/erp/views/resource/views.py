import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView

from core.erp.forms import ResourceForm, Resource
from core.security.mixins import PermissionMixin


class ResourceListView(PermissionMixin, TemplateView):
    template_name = 'resource/list.html'
    permission_required = 'view_resource'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in Resource.objects.filter():
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('resource_create')
        context['title'] = 'Listado de Materiales'
        return context


class ResourceCreateView(PermissionMixin, CreateView):
    model = Resource
    template_name = 'resource/create.html'
    form_class = ResourceForm
    success_url = reverse_lazy('resource_list')
    permission_required = 'add_resource'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                data = self.get_form().save()
            elif action == 'validate_data':
                data = {'valid': True}
                queryset = Resource.objects.all()
                type = request.POST['type']
                if type == 'name':
                    name = request.POST['name'].strip()
                    category = request.POST['category']
                    if len(category):
                        data['valid'] = not queryset.filter(name__iexact=name, category_id=category).exists()
                elif type == 'code':
                    data['valid'] = not queryset.filter(code__iexact=request.POST['code']).exists()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de un Material'
        context['action'] = 'add'
        return context


class ResourceUpdateView(PermissionMixin, UpdateView):
    model = Resource
    template_name = 'resource/create.html'
    form_class = ResourceForm
    success_url = reverse_lazy('resource_list')
    permission_required = 'change_resource'

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
                id = self.object.id
                queryset = Resource.objects.all().exclude(id=id)
                type = request.POST['type']
                if type == 'name':
                    name = request.POST['name'].strip()
                    category = request.POST['category']
                    if len(category):
                        data['valid'] = not queryset.filter(name__iexact=name, category_id=category).exists()
                elif type == 'code':
                    data['valid'] = not queryset.filter(code__iexact=request.POST['code']).exists()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de un Material'
        context['action'] = 'edit'
        return context


class ResourceDeleteView(PermissionMixin, DeleteView):
    model = Resource
    template_name = 'resource/delete.html'
    success_url = reverse_lazy('resource_list')
    permission_required = 'delete_resource'

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