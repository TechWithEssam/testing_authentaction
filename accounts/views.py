from django.shortcuts import render, redirect, get_object_or_404
from .models import User, VerificationToken
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.http import Http404, HttpResponse
from .forms import UserCreationForm, UserChangeForm, LoginForm
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
# Create your views here.


def profile_view(request, **kwargs) :
    template_name = "accounts/profile.html"
    username = kwargs.get("username")
    if username :
        try :
            obj = User.objects.get(username=username) 
        except :
            return redirect("products:not_found")
    print(request.user.username)
    context = {
        "obj" : obj
    }
    return render(request, template_name, context)


def register_view(request) :
    template_name = "accounts/register.html"
    form = UserCreationForm(request.POST or None)
    if form.is_valid() :
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        verification_token = user.verificationtoken.token
        verification_link = reverse('accounts:verify') + f'?token={verification_token}'
        send_mail(
        'Verify your email address',
        f'''
        wecome to es marketplace, 
        Please click this link to verify your email address: {settings.BASE_URL}{verification_link}''',
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,)
        messages.success(request,"check your email to activate your account")
    context = {
        "form" : form
    }
    return render(request, template_name, context)

def verify(request):
    template_name = "accounts/verify.html"
    token = request.GET.get('token')
    try:
        verification_token = VerificationToken.objects.get(token=token)
    except VerificationToken.DoesNotExist:
        return redirect("products:not_found")
    es = verification_token.user.username
    account = User.objects.get(username=es)
    account.is_active = True
    account.is_verified = True
    account.save()
    print(account.is_active)
    print(es)
    context = {
        "token" : verification_token
    }
    return render(request, template_name, context)


def login_view(request):
    template_name = 'accounts/login.html'
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid() :
            username = request.POST.get("username")
            password = request.POST.get("password")
            print(username)
            user = authenticate(request, username=username, password=password)
            if user is not None :
                login(request, user)
                return redirect("products:home")
            else :
                messages.error(request, "email or password is wrong")
    else :
        form = LoginForm()
    context = {
        "form" : form
    }
    return render(request, template_name, context)
     

def logout_view(request) :
    logout(request)
    return redirect("accounts:login")