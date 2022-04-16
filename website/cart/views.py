from django.shortcuts import render, redirect
from home.models import Product
from .models import *
from django.contrib.auth.decorators import login_required
from order.models import OrderForm


def cart_detail(request):
    carts = Cart.objects.filter(user_id=request.user.id)
    user = request.user
    form = OrderForm()
    total = 0
    for cart in carts:
        if cart.product.status is not None:
            total += cart.variant.total_price * cart.quantity
        else:
            total += cart.product.total_price * cart.quantity
    context = {
        'carts': carts,
        'total': total,
        'form': form,
        'user': user,
    }
    return render(request, 'cart/cart.html', context)


@login_required(login_url='accounts:login')
def add_cart(request, id):
    url = request.META.get('HTTP_REFERER')
    product = Product.objects.get(id=id)
    if product.status is not None:
        var_id = request.POST.get('select')
        data = Cart.objects.filter(user_id=request.user.id, variant_id=var_id)
        if data:
            check = 'yes'
        else:
            check = 'no'
    else:
        data = Cart.objects.filter(user_id=request.user.id, product_id=id)
        if data:
            check = 'yes'
        else:
            check = 'no'
    if request.method == 'POST':
        form = CartForm(request.POST)
        var_id = request.POST.get('select')
        if form.is_valid():
            info = form.cleaned_data['quantity']
            if check == 'yes':
                if product.status is not None:
                    update_shop = Cart.objects.get(user_id=request.user.id, product_id=id, variant_id=var_id)
                else:
                    update_shop = Cart.objects.get(user_id=request.user.id, product_id=id)
                update_shop.quantity += info
                update_shop.save()
            else:
                Cart.objects.create(user_id=request.user.id, product_id=id, variant_id=var_id, quantity=info)
        return redirect(url)


@login_required(login_url='accounts:login')
def remove_cart(request, id):
    url = request.META.get('HTTP_REFERER')
    Cart.objects.filter(id=id).delete()
    return redirect(url)

