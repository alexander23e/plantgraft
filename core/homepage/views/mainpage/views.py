import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.contrib.auth.models import Group
from django.db import transaction
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic import TemplateView, FormView

from config import settings
from core.erp.forms import ClientForm, ClientUserForm
from core.erp.models import Product, Category, Client, Company
from core.homepage.models import Services, Testimonials, FrequentQuestions, SocialNetworks
from core.user.models import User


class IndexView(TemplateView):
    template_name = 'mainpage/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Services.objects.filter(state=True).order_by('id')
        context['testimonials'] = Testimonials.objects.filter(state=True).order_by('id')
        context['frequent_questions'] = FrequentQuestions.objects.filter(state=True).order_by('id')
        context['products'] = Product.objects.filter().order_by('id')
        context['categories'] = Category.objects.filter().order_by('id')
        context['initial'] = True
        return context


class SignInView(FormView):
    form_class = ClientForm
    template_name = 'mainpage/sign_in.html'

    def get_form_user(self):
        form = ClientUserForm()
        if self.request.POST or self.request.FILES:
            form = ClientUserForm(self.request.POST, self.request.FILES)
        return form

    def send_email_activation(self, id):
        try:
            company = Company.objects.first()
            url = settings.LOCALHOST if not settings.DEBUG else self.request.META['HTTP_HOST']
            user = User.objects.get(pk=id)
            message = MIMEMultipart('alternative')
            message['Subject'] = 'Registro de cuenta'
            message['From'] = company.email_host
            message['To'] = user.email
            parameters = {
                'user': user,
                'company': company,
                'url': f'http://{url}/login',
            }
            html = render_to_string('mainpage/active_account_email.html', parameters)
            content = MIMEText(html, 'html')
            message.attach(content)
            server = smtplib.SMTP(company.email_host, company.email_port)
            server.starttls()
            server.login(company.email_host_user, company.email_host_password)
            server.sendmail(
                company.email_host_user, user.email, message.as_string()
            )
            server.quit()
            return True
        except:
            pass
        return False

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'create_account':
                with transaction.atomic():
                    form1 = self.get_form_user()
                    form2 = self.get_form()
                    if form1.is_valid() and form2.is_valid():
                        user = form1.save(commit=False)
                        user.username = form1.cleaned_data.get('dni')
                        user.set_password(user.dni)
                        user.save()
                        user.groups.add(Group.objects.get(pk=settings.GROUPS.get('client')))
                        form_client = form2.save(commit=False)
                        form_client.user = user
                        form_client.save()
                        if not self.send_email_activation(user.id):
                            transaction.set_rollback(True)
                            data['error'] = 'No se ha podido crear la cuenta, intenta mas tarde'
                    else:
                        if not form1.is_valid():
                            data['error'] = form1.errors
                        elif not form2.is_valid():
                            data['error'] = form2.errors
            elif action == 'validate_data':
                data = {'valid': True}
                pattern = request.POST['pattern']
                parameter = request.POST['parameter'].strip()
                queryset = Client.objects.all()
                if pattern == 'dni':
                    data['valid'] = not queryset.filter(user__dni=parameter).exists()
                elif pattern == 'mobile':
                    data['valid'] = not queryset.filter(mobile=parameter).exists()
                elif pattern == 'email':
                    data['valid'] = not queryset.filter(user__email=parameter).exists()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['frmUser'] = ClientUserForm()
        return context
