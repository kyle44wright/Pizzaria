from django.shortcuts import render, redirect
from .models import *
from .forms import *

# Create your views here.
def index(request):
    return render(request, 'pizzas/index.html')

def pizzas(request):
    pizzas = Pizza.objects.order_by('pizza_name')

    context = {'all_pizzas':pizzas}

    return render(request, 'pizzas/pizzas.html', context)

def pizza(request, pizza_id):
    p = Pizza.objects.get(id=pizza_id)
    toppings = Topping.objects.filter(pizza=p)
    new_comments = Comment.objects.filter(pizza=pizza_id).order_by('-date_added')
    image = Image.objects.filter(pizza=pizza_id)

    context = {'pizza':p, 'toppings': toppings, 'new_comments': new_comments, 'image': image}

    return render(request, 'pizzas/pizza.html', context)

def comment(request, pizza_id):
    pizza = Pizza.objects.get(id=pizza_id)

    if request.method != 'POST':
        form = CommentForm()
        
    else:
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.pizza = pizza
            comment.save()
            return redirect('pizzas:pizza',pizza_id=pizza_id)
    context = {'form':form, 'pizza':pizza}

    return render(request, 'pizzas/comment.html', context)



