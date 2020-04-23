from django import forms

from apps.core.models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'price']
    