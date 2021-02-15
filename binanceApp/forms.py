from django import forms
from binanceApp.models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('order',
                  'range_price',
                  'btc_count')
        widgets = {
            'order': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Order name'}),
            'range_price': forms. NumberInput(attrs={'class': 'form-control', 'placeholder': 'Range price'}),
            'btc_count': forms. NumberInput(attrs={'class': 'form-control', 'placeholder': 'BTC count'}),
        }
        labels = {
            'order': 'Order name',
            'range_price': 'Range price',
            'btc_count': 'BTC count',
        }

