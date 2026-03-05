from django import forms

from core.erp.choices import PRODUCT_OPTIONS, MONTHS
from core.erp.models import Employee, Client, Lot, Production, Product


class ReportForm(forms.Form):
    date_range = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }), label='Buscar por rango de fechas')

    search = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }), label='Buscador')

    employee = forms.ModelChoiceField(widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%;'
    }), queryset=Employee.objects.all(), label='Empleado')

    year = forms.CharField(widget=forms.TextInput(attrs={
        'id': 'year',
        'class': 'form-control datetimepicker-input',
        'data-toggle': 'datetimepicker',
        'data-target': '#year',
    }), label='Año')

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

    client = forms.ModelChoiceField(widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%;'
    }), queryset=Client.objects.all(), label='Cliente')

    clients = forms.ModelChoiceField(widget=forms.SelectMultiple(attrs={
        'class': 'form-control select2',
        'multiple': 'multiple',
    }), queryset=Client.objects.all(), empty_label=None, label='Clientes')

    lot = forms.ModelChoiceField(widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%;'
    }), queryset=Lot.objects.all(), label='Lote')

    production = forms.ModelChoiceField(widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%;'
    }), queryset=Production.objects.all(), label='Producción')

    product = forms.ModelChoiceField(widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%;'
    }), queryset=Product.objects.all(), label='Producto')

    product_options = forms.ChoiceField(widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%;'
    }), choices=PRODUCT_OPTIONS, label='Opciones')

    month = forms.ChoiceField(widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%;'
    }), choices=MONTHS, label='Mes')
