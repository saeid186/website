from django.shortcuts import render, redirect
from .models import *
from cart.models import Cart
from .forms import CouponForm
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponse
import requests, json
import jdatetime


def order_detail(request, order_id):
    order = Order.objects.get(id=order_id)
    form = CouponForm()
    context = {
        'order': order,
        'form': form,
    }
    return render(request, 'order/order.html', context)


def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            order = Order.objects.create(user_id=request.user.id, email=data['email'],
                                         f_name=data['f_name'], l_name=data['l_name'], address=data['address'])
            carts = Cart.objects.filter(user_id=request.user.id)
            for cart in carts:
                if cart.product.status is not None:
                    ItemOrder.objects.create(order_id=order.id, user_id=request.user.id, product_id=cart.product.id,
                                             variant_id=cart.variant.id, quantity=cart.quantity)
                else:
                    ItemOrder.objects.create(order_id=order.id, user_id=request.user.id, product_id=cart.product.id,
                                             quantity=cart.quantity)

            # Cart.objects.filter(user_id=request.user.id).delete()
            return redirect('order:order_detail', order.id)


@require_POST
def coupon_order(request, order_id):
    form = CouponForm(request.POST)
    time = jdatetime.datetime.now()
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code, start__lte=time, end__gte=time, active=True)
        except Coupon.DoesNotExist:
            messages.error(request, 'Code wrong', 'danger')
            return redirect('order:order_detail', order_id)
        order = Order.objects.get(id=order_id)
        order.discount = coupon.discount
        order.save()
    return redirect('order:order_detail', order_id)


MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
# amount = 11000  # Rial / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
# email = 'email@example.com'  # Optional
mobile = '09123456789'  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://localhost:8000/order/verify/'


def send_request(request, order_id, price):
    global amount
    email = request.user.email
    amount = price
    req_data = {
        "merchant_id": MERCHANT,
        "amount": amount,
        "callback_url": CallbackURL,
        "description": description,
        "metadata": {"mobile": mobile, "email": email}
    }
    req_header = {"accept": "application/json",
                  "content-type": "application/json'"}
    req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
        req_data), headers=req_header)
    if len(req.json()['errors']) == 0:
        authority = req.json()['data']['authority']
        return redirect(ZP_API_STARTPAY.format(authority=authority))
    else:
        e_code = req.json()['errors']['code']
        e_message = req.json()['errors']['message']
        # برای پرداخت موفق بعدا باید جایگذاری شود
        order = Order.objects.get(id=order_id)
        order.paid = True
        order.save()
        carts = ItemOrder.objects.filter(order_id=order_id)
        for cart in carts:
            if cart.product.status is None:
                product = Product.objects.get(id=cart.product.id)
                product.amount -= cart.quantity
                product.save()
            else:
                variant = Variants.objects.get(id=cart.variant.id)
                variant.amount -= cart.quantity
                variant.save()

        return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")


def verify(request):
    t_status = request.GET.get('Status')
    t_authority = request.GET['Authority']
    if request.GET.get('Status') == 'OK':
        req_header = {"accept": "application/json",
                      "content-type": "application/json'"}
        req_data = {
            "merchant_id": MERCHANT,
            "amount": amount,
            "authority": t_authority
        }
        req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
        if len(req.json()['errors']) == 0:
            t_status = req.json()['data']['code']
            if t_status == 100:
                return HttpResponse('Transaction success.\nRefID: ' + str(
                    req.json()['data']['ref_id']
                ))
            elif t_status == 101:
                return HttpResponse('Transaction submitted : ' + str(
                    req.json()['data']['message']
                ))
            else:
                return HttpResponse('Transaction failed.\nStatus: ' + str(
                    req.json()['data']['message']
                ))
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
    else:
        return HttpResponse('Transaction failed or canceled by user')

