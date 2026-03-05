from django import forms

from core.homepage.models import *


class ServicesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Services
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'description': forms.Textarea(attrs={'placeholder': 'Ingrese una descripción', 'rows': 3, 'cols': '3'}),
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


class FrequentQuestionsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['question'].widget.attrs['autofocus'] = True

    class Meta:
        model = FrequentQuestions
        fields = '__all__'
        widgets = {
            'question': forms.Textarea(attrs={'placeholder': 'Ingrese una descripción', 'rows': 3, 'cols': 3}),
            'answer': forms.Textarea(attrs={'placeholder': 'Ingrese un descripción', 'rows': 3, 'cols': 3}),
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


class SocialNetworksForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['url'].widget.attrs['autofocus'] = True

    class Meta:
        model = SocialNetworks
        fields = '__all__'
        widgets = {
            'url': forms.TextInput(attrs={'placeholder': 'Ingrese una dirección web'}),
            'code': forms.TextInput(attrs={'placeholder': 'Ingrese un código'}),
            'icon': forms.TextInput(attrs={'placeholder': 'Ingrese un icono'}),
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


class TestimonialsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['names'].widget.attrs['autofocus'] = True

    class Meta:
        model = Testimonials
        fields = '__all__'
        widgets = {
            'names': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'profession': forms.TextInput(attrs={'placeholder': 'Ingrese una profesión'}),
            'comment': forms.Textarea(attrs={'placeholder': 'Ingrese una descripción', 'rows': 3, 'cols': 3}),
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
