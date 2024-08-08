from django import forms
from .models import CartItem

class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ('quantity',)

# class BalanceForm(forms.ModelForm):
#     class Meta:
#         model = Balance
#         fields = ('amount',)