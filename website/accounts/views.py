from django.shortcuts import render, redirect, reverse
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from random import randint
from django.core.mail import EmailMessage
from django.views import View
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from order.models import ItemOrder


class EmailToken(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_active) + text_type(user.id) + text_type(timestamp))


email_generator = EmailToken()


def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(username=data['user_name'], email=data['email'],
                                            first_name=data['first_name'], last_name=data['last_name'],
                                            password=data['password_2'])
            user.is_active = False
            user.save()
            domain = get_current_site(request).domain
            uidb64 = urlsafe_base64_encode(force_bytes(user.id))
            url = reverse('accounts:active', kwargs={'uidb64': uidb64, 'token': email_generator.make_token(user)})
            link = 'http://' + domain + url
            email = EmailMessage(
                'active email',
                link,
                'saeid186django@gmail.com',
                [data['email']]
            )
            email.send(fail_silently=False)
            messages.warning(request, 'به ایمل خود مراجعه کنید', 'warning')
            return redirect('home:home')
    elif request.method == 'GET':
        form = UserRegisterForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)


class RegisterEmail(View):
    def get(self, request, uidb64, token):
        id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=id)
        if user and email_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('accounts:login')


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                user = authenticate(request, username=User.objects.get(email=data['user']),
                                    password=data['password'])
            except:
                user = authenticate(request, username=data['user'], password=data['password'])
            if user is not None:
                login(request, user)
                messages.success(request, "با موفقیت وارد شدید.", "primary")
                return redirect('home:home')
            else:
                messages.error(request, "نام کاربری یا کلمه عبور صحیح نیست.", "danger")
                return redirect('accounts:login')

    elif request.method == 'GET':
        form = UserLoginForm()
    context = {
        'form': form
    }

    return render(request, 'accounts/login.html', context)


def user_logout(request):
    logout(request)
    messages.success(request, "Logout Successfully", "warning")
    return redirect('home:home')


@login_required(login_url='accounts:login')
def user_profile(request):
    profile = Profile.objects.get(user_id=request.user.id)
    context = {
        'profile': profile
    }
    return render(request, 'accounts/profile.html', context)


@login_required(login_url='accounts:login')
def user_update(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Update Successfully", "success")
            return redirect('accounts:profile')
    elif request.method == "GET":
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'accounts/update.html', context)


def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Password change Success Please login with new password", "success")
            return redirect('accounts:profile')
        else:
            messages.error(request, "Password does not changed", "danger")
            return redirect('accounts:change')
    elif request.method == "GET":
        form = PasswordChangeForm(request.user)
    context = {
        'form': form
    }
    return render(request, 'accounts/change.html', context)


def phone(request):
    global random_code , phone
    if request.method == "POST":
        form = PhoneForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            phone = f"0{data['phone']}"
            random_code = randint(10000, 99999)
            print(random_code)
            return redirect('accounts:verify')
    elif request.method == "GET":
        form = PhoneForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/phone.html', context)


def verify(request):
    if request.method == "POST":
        form = CodeForm(request.POST)
        if form.is_valid():
            if random_code == form.cleaned_data['code']:
                profile = Profile.objects.get(phone=phone)
                user = User.objects.get(profile__id=profile.id)
                login(request, user)
                messages.success(request, "Hi user")
                return redirect('home:home')
            else:
                messages.error(request, "Wrong code", "danger")
        else:
            messages.error(request, "form invalid")
    elif request.method == "GET":
        form = CodeForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/code.html', context)


def favourite(request):
    products = request.user.fa_user.all()
    context = {
        'products': products,
    }
    return render(request, 'accounts/favourite.html', context)


def history(request):
    data = ItemOrder.objects.filter(user_id=request.user.id)
    context = {
        'data': data,
    }
    return render(request, 'accounts/history.html', context)


class ResetPassword(auth_views.PasswordResetView):
    template_name = 'accounts/reset.html'
    success_url = reverse_lazy('accounts:reset_done')
    email_template_name = 'accounts/link.html'


class ResetPasswordDone(auth_views.PasswordResetDoneView):
    template_name = 'accounts/done.html'


class ConfirmPassword(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/confirm.html'
    success_url = reverse_lazy('accounts:complete')


class Complete(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/complete.html'

