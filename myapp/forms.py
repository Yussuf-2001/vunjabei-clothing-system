from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['quantity', 'phone', 'address']
        widgets = {
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'value': '1'
            }),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Namba ya Simu (M-Pesa/Tigo)'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Mahali unapoishi / Maelekezo ya kufika'}),
        }