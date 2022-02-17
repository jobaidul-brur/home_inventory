from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Item, Category


@login_required
def create_item(request):
    if request.method == 'POST':
        data = request.POST
        category_id = data['category']
        category = Category.objects.get(id=category_id)
        name = data['name']
        price = data['price']
        description = data['description']
        image = data['image']
        Item.objects.create(category=category, name=name, price=price, description=description, image=image,
                            user=request.user)
        return HttpResponseRedirect(reverse('inventory:list'))
    else:
        categories = Category.objects.all()
        return render(request, 'product_form.html', {'categories': categories})


@login_required
def edit_item(request, item_id):
    if not Item.objects.filter(id=item_id).exists():
        return HttpResponse('Item not found')
    item = Item.objects.get(id=item_id)
    if request.method == 'POST':
        data = request.POST
        item.category_id = data['category']
        item.name = data['name']
        item.price = data['price']
        item.description = data['description']
        item.image = data['image']
        item.save()
        return HttpResponseRedirect(reverse('inventory:list'))
    else:
        categories = Category.objects.all()
        return render(request, 'product_form.html', {'categories': categories, 'item': item})


@login_required
def show_item_list(request, message=None):
    user = request.user
    if user.is_superuser:
        items = Item.objects.all()
    else:
        items = Item.objects.filter(user=user)
    return render(request, 'item_list.html', {'items': items, 'message': message})


@login_required
def delete_item(request, item_id):
    if not Item.objects.filter(id=item_id).exists():
        return HttpResponse('Item not found')
    if request.user == Item.objects.get(id=item_id).user or request.user.is_superuser:
        Item.objects.get(id=item_id).delete()
        return HttpResponseRedirect(reverse('inventory:list', args=('Item has been deleted',)))
    return HttpResponse('You are not allowed to delete this item')
