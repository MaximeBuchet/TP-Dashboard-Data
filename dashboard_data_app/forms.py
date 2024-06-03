from django import forms
from .models import Product

class LoginForm(forms.Form):
    username = forms.CharField(max_length=220)
    password = forms.CharField(max_length=220, widget=forms.PasswordInput)


class UploadFileForm(forms.Form):
    file = forms.FileField(label='File name :')

class AddSalesForm(forms.Form):
    product = forms.ModelChoiceField(Product.objects.order_by("name"),label='Product :')
    price = forms.CharField(max_length=220, widget=forms.NumberInput)
    quantity = forms.CharField(max_length=220, widget=forms.NumberInput)

class PerformanceForm(forms.Form):
    chart_type = forms.ChoiceField(choices=[('bar', 'Bar plot'), ('line', 'Line plot'), ('count', 'Count plot')])
    date_from = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Date from :", required=False)
    date_to = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Date to :", required=False)


