from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.utils import timezone

from apps.core.models import Item, OrderItem, Order
from apps.core.forms import ItemForm

def list_item(request):
    print('called this')
    items = Item.objects.all()
    print(items)
    return render(request, 'home.html', {'items':items})

def create_item(request):
    if request.method == 'GET':
        form = ItemForm()
        return render(request, 'home.html', {'form': form})
    elif request.method == 'POST':
        form = ItemForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            return redirect(reverse('list_item'))
        else:
            return redirect(request, 'home.html', {'form': form})

def detail_item(request, id):
    item = get_object_or_404(Item, id=id)
    return render(request, 'detail_item.html', {'item': item})

def update_item(request, id):
    item = get_object_or_404(Item, id=id)
    if request.method=='GET':
        form = ItemForm(instance=item)
        return render(request, 'update_item.html', {'form': form})
    if request.method=='POST':
        form = ItemForm(request.POST or None, request.FILES or None, instance=item)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            print('valid form')
            return redirect(reverse('detail_item', kwargs={'id':item.id}))
        else:
            return render(request, 'update_item.html', {'form': form})


def delete_item(request,id):
    item = get_object_or_404(Item, id=id)
    item.delete()
    print('here now')
    return redirect(reverse('list_item'))


def add_to_cart(request, id):
    print('inside cart')
    item = get_object_or_404(Item, id=id)
    order_item, status = OrderItem.objects.get_or_create(item=item, user=request.user)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        print('order qs exists')
        order = order_qs[0]
        if order.items.filter(item = item).exists():
            print('item exists')
            order_item.quantity += 1
            order_item.save()
            print(order_item.quantity)
        else:
            print('item doesnot exists')
            order.items.add(order_item)
    else:
        print('order of a user dowsnot exists')
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date = ordered_date)
        print(order)
        order.items.add(order_item)
    print('inside cart bottom')
    return redirect(reverse('detail_item', kwargs={
        'id': id,
    }))

def remove_from_cart(request, id):
    item = get_object_or_404(Item, id=id)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item=item).exists():
            order_item = OrderItem.objects.filter(item__id=item.id, user=request.user)[0]
            order.items.remove(order_item)
            print('Item successfully removed', item)
        else:
            print('Item doesnot exists')
            return redirect('detail_item', id=id)
    else:
        print('Order doesnot exists, Unable to delete')
        return redirect('detail_item', id=id)
    print('That user donot have any orders')
    return redirect('detail_item', id=id)
        
        