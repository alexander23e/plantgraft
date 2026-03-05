import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView

from core.homepage.forms import FrequentQuestions, FrequentQuestionsForm
from core.security.mixins import PermissionMixin


class FrequentQuestionsListView(PermissionMixin, TemplateView):
    template_name = 'frequent_questions/list.html'
    permission_required = 'view_frequent_questions'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in FrequentQuestions.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('frequent_questions_create')
        context['title'] = 'Listado de Preguntas y Frecuentes'
        return context


class FrequentQuestionsCreateView(PermissionMixin, CreateView):
    model = FrequentQuestions
    template_name = 'frequent_questions/create.html'
    form_class = FrequentQuestionsForm
    success_url = reverse_lazy('frequent_questions_list')
    permission_required = 'add_frequent_questions'

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
        context['title'] = 'Nuevo registro de una Pregunta Frecuente'
        context['action'] = 'add'
        return context


class FrequentQuestionsUpdateView(PermissionMixin, UpdateView):
    model = FrequentQuestions
    template_name = 'frequent_questions/create.html'
    form_class = FrequentQuestionsForm
    success_url = reverse_lazy('frequent_questions_list')
    permission_required = 'change_frequent_questions'

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
        context['title'] = 'Edición de una Pregunta Frecuente'
        context['action'] = 'edit'
        return context


class FrequentQuestionsDeleteView(PermissionMixin, DeleteView):
    model = FrequentQuestions
    template_name = 'frequent_questions/delete.html'
    success_url = reverse_lazy('frequent_questions_list')
    permission_required = 'delete_frequent_questions'

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
