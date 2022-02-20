import operator

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Item, Category


@login_required
def create_item(request):
    if request.method == 'POST':
        data = request.POST
        category_id = data.get('category')
        category = Category.objects.get(id=category_id)
        name = data.get('name')
        price = data.get('price').replace(',', '')
        description = data.get('description')
        image = data.get('image')

        if float(price) >= 1_000_000_000:
            message = 'Price must be less than 1,000,000,000'
            categories = sorted(Category.objects.all(), key=operator.attrgetter('name'))
            return render(request, 'product_form.html', {'categories': categories, 'message': message, 'edit': False})

        Item.objects.create(category=category, name=name, price=price, description=description, image=image,
                            user=request.user)
        return HttpResponseRedirect(reverse('inventory:list', args=('Item Created Successfully',)))
    else:
        categories = sorted(Category.objects.all(), key=operator.attrgetter('name'))
        return render(request, 'product_form.html', {'categories': categories, 'edit' : False})


@login_required
def edit_item(request, item_id):
    if not Item.objects.filter(id=item_id).exists():
        return HttpResponse('Item not found')
    item = Item.objects.get(id=item_id)
    if request.method == 'POST':
        data = request.POST

        if float(data.get('price').replace(",", "")) >= 1_000_000_000:
            message = 'Price must be less than 1,000,000,000'
            categories = sorted(Category.objects.all(), key=operator.attrgetter('name'))
            return render(request, 'product_form.html', {'categories': categories, 'item': item, 'message': message, 'edit': True})

        item.category_id = data.get('category')
        item.name = data.get('name')
        item.price = data.get('price').replace(",", "")
        item.description = data.get('description')
        item.image = data.get('image')

        item.save()
        return HttpResponseRedirect(reverse('inventory:list'))
    else:
        categories = sorted(Category.objects.all(), key=operator.attrgetter('name'))
        return render(request, 'product_form.html', {'categories': categories, 'item': item, 'edit' : True})


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
