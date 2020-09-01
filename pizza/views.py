from django.shortcuts import render
from .forms import PizzaForm, MultiplePizzaForm
from .models import Pizza, Size, Crust
from django.forms import formset_factory


# Create your views here.
def home(request):
    return render(request, 'pizza/home.html')


def order(request):
    # It's a flat price increase per topping based on the size of the pizza
    # Maybe like +$0.80 per on small, $1 on medium, $1.30 on large
    # Thin, regular, thick, cheesy
    # +$0, +$0, +$1, +$2
    multiple_form = MultiplePizzaForm()
    note = None
    cost = 0
    if request.method == "POST":
        filled_form = PizzaForm(request.POST)
        if filled_form.is_valid():
            created_pizza = filled_form.save()
            created_pizza_pk = created_pizza.id
            size = filled_form.cleaned_data['size']
            toppings = filled_form.cleaned_data['toppings']
            crust = filled_form.cleaned_data['crust']
            quantity = filled_form.cleaned_data['quantity']
            number_of_toppings = toppings.count()
            cost = number_of_toppings * Size.objects.get(title=size).cost
            cost += Crust.objects.get(type=crust).cost
            cost *= quantity
            note = f"Your {quantity} {size}, {crust} crust pizza with {number_of_toppings} toppings have been ordered " \
                   f"for ${cost}. "
        else:
            created_pizza_pk = None
            note = "Pizza order has failed. Try again!"
        return render(request, 'pizza/order.html',
                      {'created_pizza_pk': created_pizza_pk, 'pizzaForm': filled_form, 'note': note,
                       'multiple_form': multiple_form})
    else:
        form = PizzaForm()
        return render(request, 'pizza/order.html', {'pizzaForm': form, 'multiple_form': multiple_form, 'note': None})


def pizzas(request):
    number_of_pizzas = 2
    filled_multiple_pizza_form = MultiplePizzaForm(request.GET)
    if filled_multiple_pizza_form.is_valid():
        number_of_pizzas = filled_multiple_pizza_form.cleaned_data['number']
    PizzaFormSet = formset_factory(PizzaForm, extra=number_of_pizzas)
    formset = PizzaFormSet()
    note = ""
    total_cost = 0
    if request.method == "POST":
        filled_formset = PizzaFormSet(request.POST)
        if filled_formset.is_valid():
            for form in filled_formset:
                form.save()
                size = form.cleaned_data['size']
                toppings = form.cleaned_data['toppings']
                crust = form.cleaned_data['crust']
                quantity = form.cleaned_data['quantity']
                number_of_toppings = toppings.count()
                cost = number_of_toppings * Size.objects.get(title=size).cost
                cost += Crust.objects.get(type=crust).cost
                cost *= quantity
                total_cost += cost
                note += f"{quantity} {size}, {crust} crust pizza with {number_of_toppings} for ${cost}."
            note += f"Total Cost: {total_cost}"
        else:
            note = 'Order unsuccessful! Please try again!'
        return render(request, 'pizza/pizzas.html', {'note': note, 'formset': formset})
    else:
        return render(request, 'pizza/pizzas.html', {'formset': formset, 'note': None})


def edit_order(request, pk):
    pizza = Pizza.objects.get(pk=pk)
    form = PizzaForm(instance=pizza)
    if request.method == "POST":
        filled_form = PizzaForm(request.POST, instance=pizza)
        if filled_form.is_valid():
            filled_form.save()
            form = filled_form
            note = "Order has been updated."
            return render(request, 'pizza/edit_order.html', {'pizzaForm': form, 'pizza': pizza, 'note': note})
    return render(request, 'pizza/edit_order.html', {'pizzaForm': form, 'pizza': pizza, 'note': None})


def pricing(request):
    return render(request, 'pizza/pricing.html', {})
