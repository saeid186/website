from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import *
from .forms import SearchForm
from django.db.models import Q
from cart.models import *
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from .filters import ProductFilter
from django.contrib import messages


def home(request):
    category = Category.objects.filter(sub_cat=False)
    gallery = Gallery.objects.all()
    create = Product.objects.all().order_by('-create')[:6]
    context = {
        'category': category,
        'gallery': gallery,
        'create': create,
    }
    return render(request, 'home/home.html', context)


def all_product(request, slug=None, id=None):
    products = Product.objects.all()
    filter = ProductFilter(request.GET, queryset=products)
    products = filter.qs
    paginator = Paginator(products, 2)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    category = Category.objects.filter(sub_cat=False)
    form = SearchForm()
    if 'search' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            data = form.cleaned_data['search']
            products = products.filter(Q(name__icontains=data))
            paginator = Paginator(products, 3)
            page_num = request.GET.get('page')
            page_obj = paginator.get_page(page_num)
    if slug and id:
        data = get_object_or_404(Category, slug=slug, id=id)
        products = products.filter(category=data)
        paginator = Paginator(products, 3)
        page_num = request.GET.get('page')
        page_obj = paginator.get_page(page_num)
    context = {
        'products': page_obj,
        'category': category,
        'form': form,
        'page_num': page_num,
        'filter': filter,
    }
    return render(request, 'home/product.html', context)


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    comment_form = CommentForm()
    comments = Comment.objects.filter(product_id=id, is_reply=False)
    reply_form = ReplyForm()
    similar = product.tags.similar_objects()[:2]
    images = Images.objects.filter(product_id=id)
    cart_form = CartForm()
    is_like = False
    if product.like.filter(id=request.user.id).exists():
        is_like = True
    is_unlike = False
    if product.unlike.filter(id=request.user.id).exists():
        is_unlike = True
    is_favourite = False
    if product.favourite.filter(id=request.user.id).exists():
        is_favourite = True
    if product.status is not None:
        if request.method == "POST":
            variant = Variants.objects.filter(product_variant_id=id)
            var_id = request.POST.get('select')
            variants = Variants.objects.get(id=var_id)
        elif request.method == "GET":
            variant = Variants.objects.filter(product_variant_id=id)
            variants = Variants.objects.get(id=variant[0].id)
        context = {
            'product': product,
            'variant': variant,
            'variants': variants,
            'similar': similar,
            'images': images,
            'cart_form': cart_form,
            'is_favourite': is_favourite,
            'is_like': is_like,
            'is_unlike': is_unlike,
            'comment_form': comment_form,
            'comments': comments,
            'reply_form': reply_form,
        }
        return render(request, 'home/detail.html', context)
    else:
        context = {
            'product': product,
            'similar': similar,
            'images': images,
            'cart_form': cart_form,
            'is_favourite': is_favourite,
            'is_like': is_like,
            'is_unlike': is_unlike,
            'comment_form': comment_form,
            'comments': comments,
            'reply_form': reply_form,
        }
        return render(request, 'home/detail.html', context)


def product_search(request):
    products = Product.objects.all()
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['search']
            if data.isdigit():
                products = products.filter(Q(discount__exact=data) | Q(unit_price__exact=data))
            else:
                products = products.filter(name__icontains=data)
                context = {
                    'products': products,
                    'form': form,
                }
            return render(request, 'home/product.html', context)


def favourite_product(request, id):
    url = request.META.get('HTTP_REFERER')
    product = Product.objects.get(id=id)
    is_favourite = False
    if product.favourite.filter(id=request.user.id).exists():
        product.favourite.remove(request.user)
        is_favourite = False
    else:
        product.favourite.add(request.user)
        is_favourite = True
    return redirect(url)


def contact(request):
    if request.method == 'POST':
        subject = request.POST['subject']
        email = request.POST['email']
        message = request.POST['message']
        body = f"subject: {subject} \n email: {email} \n message: {message}"
        form = EmailMessage(
            'Contact form',
            body,
            'test',
            ('saeid186django@gmail.com',),
        )
        form.send(fail_silently=False)
    return render(request, 'home/contact.html')


def product_like(request, id):
    url = request.META.get('HTTP_REFERER')
    product = get_object_or_404(Product, id=id)
    is_like = False
    if product.like.filter(id=request.user.id).exists():
        product.like.remove(request.user)
        is_like = False
    else:
        product.like.add(request.user)
        is_like = True
    return redirect(url)


def product_unlike(request, id):
    url = request.META.get('HTTP_REFERER')
    product = get_object_or_404(Product, id=id)
    is_unlike = False
    if product.unlike.filter(id=request.user.id).exists():
        product.unlike.remove(request.user)
        is_unlike = False
    else:
        product.unlike.add(request.user)
        is_unlike = True
    return redirect(url)


def product_comment(request, id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            data = comment_form.cleaned_data
            Comment.objects.create(comment=data['comment'], rate=data['rate'],
                                   user_id=request.user.id, product_id=id)
            messages.success(request, 'کامنت شما با موفقیت ثبت شد', 'success')
        return redirect(url)


def product_reply(request, id, comment_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        reply_form = ReplyForm(request.POST)
        if reply_form.is_valid():
            data = reply_form.cleaned_data
            Comment.objects.create(comment=data['comment'], user_id=request.user.id, product_id=id,
                                   reply_id=comment_id, is_reply=True)
            return redirect(url)


def test(request):
    return render(request, 'home/test.html')

