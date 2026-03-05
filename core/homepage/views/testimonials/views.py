import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView

from core.homepage.forms import Testimonials, TestimonialsForm
from core.security.mixins import PermissionMixin


class TestimonialsListView(PermissionMixin, TemplateView):
    template_name = 'testimonials/list.html'
    permission_required = 'view_testimonials'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in Testimonials.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('testimonials_create')
        context['title'] = 'Listado de Testimonios'
        return context


class TestimonialsCreateView(PermissionMixin, CreateView):
    model = Testimonials
    template_name = 'testimonials/create.html'
    form_class = TestimonialsForm
    success_url = reverse_lazy('testimonials_list')
    permission_required = 'add_testimonials'

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
        context['title'] = 'Nuevo registro de un Testimonio'
        context['action'] = 'add'
        return context


class TestimonialsUpdateView(PermissionMixin, UpdateView):
    model = Testimonials
    template_name = 'testimonials/create.html'
    form_class = TestimonialsForm
    success_url = reverse_lazy('testimonials_list')
    permission_required = 'change_testimonials'

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
        context['title'] = 'Edición de un Testimonio'
        context['action'] = 'edit'
        return context


class TestimonialsDeleteView(PermissionMixin, DeleteView):
    model = Testimonials
    template_name = 'testimonials/delete.html'
    success_url = reverse_lazy('testimonials_list')
    permission_required = 'delete_testimonials'

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
