from django.shortcuts import render
from .forms import PizzaForm

# Create your views here.
def home(request):
    return render(request,'pizza/home.html')

def order(request):
    if request.method=="POST":
        filled_form=PizzaForm(request.POST)
        if filled_form.is_valid():
            note = "Thanks for ordering! Your {size} {topping1} and {topping2} pizza is on its way!".format(size=filled_form.cleaned_data["size"],
            topping1=filled_form.cleaned_data['topping1'],
            topping2=filled_form.cleaned_data['topping2'])
            newForm = PizzaForm()
            return render(request, 'pizza/order.html',{'pizzaForm':newForm, 'note':note})
    else:    
        form=PizzaForm()
        return render(request,'pizza/order.html',{'pizzaForm':form})