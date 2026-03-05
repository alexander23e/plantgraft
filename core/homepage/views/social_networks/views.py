import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView

from core.homepage.forms import SocialNetworks, SocialNetworksForm
from core.security.mixins import PermissionMixin


class SocialNetworksListView(PermissionMixin, TemplateView):
    template_name = 'social_networks/list.html'
    permission_required = 'view_social_networks'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in SocialNetworks.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('social_networks_create')
        context['title'] = 'Listado de Redes Sociales'
        return context


class SocialNetworksCreateView(PermissionMixin, CreateView):
    model = SocialNetworks
    template_name = 'social_networks/create.html'
    form_class = SocialNetworksForm
    success_url = reverse_lazy('social_networks_list')
    permission_required = 'add_social_networks'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                data = self.get_form().save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de una Red Social'
        context['action'] = 'add'
        return context


class SocialNetworksUpdateView(PermissionMixin, UpdateView):
    model = SocialNetworks
    template_name = 'social_networks/create.html'
    form_class = SocialNetworksForm
    success_url = reverse_lazy('social_networks_list')
    permission_required = 'change_social_networks'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                data = self.get_form().save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de una Red Social'
        context['action'] = 'edit'
        return context


class SocialNetworksDeleteView(PermissionMixin, DeleteView):
    model = SocialNetworks
    template_name = 'social_networks/delete.html'
    success_url = reverse_lazy('social_networks_list')
    permission_required = 'delete_social_networks'

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
