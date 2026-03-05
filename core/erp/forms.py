from django import forms

from .models import *


class CompanyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True
        for i in self.visible_fields():
            i.field.widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = Company
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'ruc': forms.TextInput(attrs={'placeholder': 'Ingrese un ruc'}),
            'mobile': forms.TextInput(attrs={'placeholder': 'Ingrese un teléfono celular'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Ingrese un teléfono convencional'}),
            'email': forms.TextInput(attrs={'placeholder': 'Ingrese un email'}),
            'address': forms.TextInput(attrs={'placeholder': 'Ingrese una dirección'}),
            'website': forms.TextInput(attrs={'placeholder': 'Ingrese una dirección web'}),
            'description': forms.Textarea(attrs={'placeholder': 'Ingrese una descripción', 'rows': 3, 'cols': 3}),
            'mission': forms.Textarea(attrs={'placeholder': 'Ingrese una descripción', 'rows': 3, 'cols': 3}),
            'vision': forms.Textarea(attrs={'placeholder': 'Ingrese una descripción', 'rows': 3, 'cols': 3}),
            'about_us': forms.Textarea(attrs={'placeholder': 'Ingrese una descripción', 'rows': 3, 'cols': 3}),
            'iva': forms.TextInput(),
            'latitude': forms.TextInput(attrs={'placeholder': 'Ingrese una latitud'}),
            'longitude': forms.TextInput(attrs={'placeholder': 'Ingrese una longitud'}),
            'email_host': forms.TextInput(attrs={'placeholder': 'Ingrese el servidor de correo'}),
            'email_port': forms.TextInput(attrs={'placeholder': 'Ingrese el puerto de servidor de correo'}),
            'email_host_user': forms.TextInput(attrs={'placeholder': 'Ingrese el username del servidor de correo'}),
            'email_host_password': forms.TextInput(attrs={'placeholder': 'Ingrese el password del servidor de correo'}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ProviderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Provider
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'ruc': forms.TextInput(attrs={'placeholder': 'Ingrese un número de ruc'}),
            'mobile': forms.TextInput(attrs={'placeholder': 'Ingrese un teléfono celular'}),
            'address': forms.TextInput(attrs={'placeholder': 'Ingrese una dirección'}),
            'email': forms.TextInput(attrs={'placeholder': 'Ingrese un email'}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                instace = super().save()
                data = instace.toJSON()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class EmployeeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['names'].widget.attrs['autofocus'] = True
        self.fields['headings'].queryset = Headings.objects.filter(state=True)

    class Meta:
        model = Employee
        fields = '__all__'
        widgets = {
            'names': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'dni': forms.TextInput(attrs={'placeholder': 'Ingrese un número de cédula'}),
            'mobile': forms.TextInput(attrs={'placeholder': 'Ingrese un teléfono celular'}),
            'address': forms.TextInput(attrs={'placeholder': 'Ingrese una dirección'}),
            'email': forms.TextInput(attrs={'placeholder': 'Ingrese un email'}),
            'rmu': forms.TextInput(),
            'headings': forms.SelectMultiple(attrs={'class': 'select2', 'multiple': 'multiple', 'style': 'width:100%'})
        }
        exclude = ['date_joined']

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                instace = super().save()
                data = instace.toJSON()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class HeadingsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Headings
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'percent': forms.TextInput(),
            'type': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'calculation_method': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
        }
        exclude = ['valor']

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class SalaryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Salary
        fields = '__all__'
        widgets = {
            'year': forms.TextInput(attrs={
                'class': 'form-control datetimepicker-input',
                'data-toggle': 'datetimepicker',
                'data-target': '#year',
                'value': datetime.now().year
            }),
            'month': forms.Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%;'
            }),
        }

    year_month = forms.CharField(widget=forms.TextInput(
        attrs={
            'autocomplete': 'off',
            'placeholder': 'MM / AA',
            'class': 'form-control datetimepicker-input',
            'id': 'year_month',
            'data-toggle': 'datetimepicker',
            'data-target': '#year_month',
        }
    ), label='Año/Mes')


class AssistanceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    date_joined = forms.DateField(input_formats=['%Y-%m-%d'], widget=forms.DateInput(format='%Y-%m-%d', attrs={
        'class': 'form-control datetimepicker-input',
        'id': 'date_joined',
        'value': datetime.now().strftime('%Y-%m-%d'),
        'data-toggle': 'datetimepicker',
        'data-target': '#date_joined'
    }), label='Fecha de asistencia')

    date_range = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off',
    }), label='Fecha de inicio y finalización')


class CategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class LotForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Lot
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'code': forms.TextInput(attrs={'placeholder': 'Ingrese un código'}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ResourceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Resource
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'code': forms.TextInput(attrs={'placeholder': 'Ingrese un código'}),
            'category': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'price': forms.TextInput(),
        }
        exclude = ['stock']

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'code': forms.TextInput(attrs={'placeholder': 'Ingrese un código'}),
            'type': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'description': forms.Textarea(attrs={'placeholder': 'Ingrese una descripción', 'rows': 3, 'cols': 3})
        }
        exclude = ['stock']

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class PurchaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['provider'].queryset = Provider.objects.none()

    class Meta:
        model = Purchase
        fields = '__all__'
        widgets = {
            'number': forms.TextInput(attrs={'placeholder': 'Ingrese un número de factura', 'class': 'form-control', 'autocomplete': 'off'}),
            'provider': forms.Select(attrs={'class': 'custom-select select2'}),
            'date_joined': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'date_joined',
                'value': datetime.now().strftime('%Y-%m-%d'),
                'data-toggle': 'datetimepicker',
                'data-target': '#date_joined'
            }),
            'subtotal': forms.TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off'
            }),
        }


class StageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['step'].widget.attrs['autofocus'] = True

    class Meta:
        model = Stage
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'color': forms.TextInput(attrs={'placeholder': 'Ingrese un color'}),
            'percent': forms.TextInput(),
            'description': forms.Textarea(attrs={'placeholder': 'Ingrese una descripción', 'rows': 3, 'cols': '3'}),
            'step': forms.TextInput()
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ClientForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            'mobile': forms.TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off',
                'placeholder': 'Ingrese un número de teléfono',
            }),
            'birthdate': forms.DateInput(attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'birthdate',
                'value': datetime.now().strftime('%Y-%m-%d'),
                'data-toggle': 'datetimepicker',
                'data-target': '#birthdate'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off',
                'placeholder': 'Ingrese una dirección'
            }),
        }
        exclude = ['user']


class ClientUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.visible_fields():
            if type(i.field) in [forms.CharField, forms.ImageField, forms.FileField, forms.EmailField]:
                i.field.widget.attrs.update({
                    'class': 'form-control',
                    'autocomplete': 'off'
                })
        self.fields['names'].widget.attrs['autofocus'] = True

    class Meta:
        model = User
        fields = 'names', 'dni', 'email', 'image'
        widgets = {
            'names': forms.TextInput(attrs={'placeholder': 'Ingrese sus nombres'}),
            'dni': forms.TextInput(attrs={'placeholder': 'Ingrese su número de cédula'}),
            'email': forms.TextInput(attrs={'placeholder': 'Ingrese su correo electrónico'}),
        }
        exclude = ['username', 'groups', 'is_active', 'is_change_password', 'is_staff', 'user_permissions', 'date_joined', 'last_login', 'is_superuser', 'email_reset_token']


class PromotionsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['end_date'].widget.attrs['autofocus'] = True

    class Meta:
        model = Promotions
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'start_date',
                'value': datetime.now().strftime('%Y-%m-%d'),
                'data-toggle': 'datetimepicker',
                'data-target': '#start_date'
            }),
            'end_date': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'end_date',
                'value': datetime.now().strftime('%Y-%m-%d'),
                'data-toggle': 'datetimepicker',
                'data-target': '#end_date'
            }),
        }
        exclude = ['state']

    date_range = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }), label='Fecha de inicio y finalización')


class LoansForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['employee'].widget.attrs['autofocus'] = True

    class Meta:
        model = Loans
        fields = '__all__'
        widgets = {
            'employee': forms.Select(attrs={'class': 'custom-select select2'}),
            'date_joined': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'date_joined',
                'value': datetime.now().strftime('%Y-%m-%d'),
                'data-toggle': 'datetimepicker',
                'data-target': '#date_joined'
            }),
            'valor': forms.TextInput(),
            'quota': forms.TextInput(),
            'role_discount': forms.TextInput(attrs={'readonly': True}),
        }
        exclude = ['saldo', 'state']

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ProductionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['lot'].widget.attrs['autofocus'] = True

    class Meta:
        model = Production
        fields = '__all__'
        widgets = {
            'lot': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
        }
        exclude = ['start_date', 'end_date', 'state']

    date_range = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}), label='Fecha de inicio/finalización')

    date_joined = forms.CharField(widget=forms.DateInput(format='%Y-%m-%d', attrs={
        'class': 'form-control datetimepicker-input',
        'id': 'date_joined',
        'value': datetime.now().strftime('%Y-%m-%d'),
        'data-toggle': 'datetimepicker',
        'data-target': '#date_joined'
    }), label='Fecha de registro')


class ProductionStagesForm(forms.Form):
    production = forms.ModelChoiceField(widget=forms.Select(attrs={
        'class': 'form-control select2', 'style': 'width: 100%;'
    }), required=True, queryset=Production.objects.filter(), label='Producción')

    lot = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'disabled': True
    }), label='Lote')


class HarvestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['production'].widget.attrs['autofocus'] = True

    class Meta:
        model = ProductionProducts
        fields = '__all__'
        widgets = {
            'production': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'})
        }

    date_joined = forms.CharField(widget=forms.DateInput(format='%Y-%m-%d', attrs={
        'class': 'form-control datetimepicker-input',
        'id': 'date_joined',
        'value': datetime.now().strftime('%Y-%m-%d'),
        'data-toggle': 'datetimepicker',
        'data-target': '#date_joined'
    }), label='Fecha de registro')


class SaleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client'].queryset = Client.objects.none()

    class Meta:
        model = Sale
        fields = '__all__'
        widgets = {
            'client': forms.Select(attrs={'class': 'custom-select select2'}),
            'type': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'date_joined': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'date_joined',
                'value': datetime.now().strftime('%Y-%m-%d'),
                'data-toggle': 'datetimepicker',
                'data-target': '#date_joined'
            }),
            'subtotal': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'disabled': True
            }),
            'iva': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'disabled': True
            }),
            'total_iva': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'disabled': True
            }),
            'total': forms.TextInput(attrs={
                'class': 'form-control',
                'disabled': True
            }),
        }

    voucher = forms.FileField(widget=forms.FileInput(attrs={
        'class': 'form-control',
    }), required=True, label='Comprobante')

    customer_names = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'disabled': True
    }), label='Cliente')

    customer_dni = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'disabled': True
    }), label='Número de cedula')
