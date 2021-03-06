from django import forms
from .models import Pizza,Size

# class PizzaForm(forms.Form):
#     topping1 = forms.CharField(label='Topping 1', max_length=100)
#     topping2 = forms.CharField(label='Topping 2', max_length=100)
#     size= forms.ChoiceField(label="Size", choices=[("Small","Small"),("Medium","Medium"), ("Large","Large")])

class PizzaForm(forms.ModelForm):
    class Meta:
        model=Pizza
        fields=['toppings','crust','size','quantity']
        widgets = {'toppings': forms.CheckboxSelectMultiple}
        # db_table = ''
        # managed = True
        # verbose_name = 'PizzaForm'
        # verbose_name_plural = 'PizzaForms'

class MultiplePizzaForm(forms.Form):
    number=forms.IntegerField(min_value=2, max_value=10)