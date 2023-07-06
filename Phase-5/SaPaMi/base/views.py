from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET, require_POST
from django.http import HttpResponseBadRequest
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User, Patient, HealthCenter
from .forms import UserForm, FilterForm
from packages.models import TherapeuticPackage


def my404(request, exception):
    return render(request, '404.html')


@require_GET
def home(request):
    fform = FilterForm(request.GET)
    if fform.is_valid():
        d = fform.cleaned_data
    else:
        d = fform.data
    if d['price_min'] is None:
        d['price_min'] = 0
    if d['price_max'] is None:
        d['price_max'] = 1000
    packages = TherapeuticPackage.objects.filter(
        name__icontains=d['package_name'],
        health_center__name__icontains=d['center_name'],
        approximate_price__gte=d['price_min'],
        approximate_price__lte=d['price_max'],
    )
    if d['work_field'] and d['work_field'] != 'all':
        packages = packages.filter(
            health_center__work_fields__iexact=d['work_field'],
        )
    return render(request, 'base/home.html', {'packages': packages, 'fform': fform})


@require_GET
def cas(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'base/cas.html', {
        'lform': AuthenticationForm(),
        'sform': UserCreationForm(),
    })


@require_POST
def cas_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = AuthenticationForm(request.POST)
    if form.is_valid():
        user = form.get_user()
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Wrong username/password')
    else:
        messages.error(request, 'User does not exist')

    return render(request, 'base/cas.html', {'lform': form})
    # username = request.POST.get('username').lower()
    # password = request.POST.get('password')
    # try:
    #     user = User.objects.get(username=username)
    # except:
    #     messages.error(request, 'User does not exist')
    #     return redirect('cas')
    # user = authenticate(request, username=username, password=password)


@login_required(login_url='cas')
def cas_logout(request):
    logout(request)
    return redirect('home')


@require_POST
def cas_signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = UserCreationForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        user.username = user.username.lower()
        user.save()
        login(request, user)
        return redirect("home")
    else:
        messages.error(request, "An error occour  during registration")

    return render(request, "base/register.html", {"form": form})
    # username = request.POST.get('username').lower()
    # password = request.POST.get('password')
    # usertype = request.POST.get('usertype')
    # ssn: str = request.POST.get('ssn')
    # if None in (username, password, usertype, ssn):
    #     return HttpResponseBadRequest()
    # if not ssn.isdigit():
    #     messages.error(request, 'SSN should be a number')
    #     return redirect('cas')

    # try:
    #     user = User.objects.get(username=username)
    #     messages.error(request, 'Username is already taken')
    #     return redirect('cas')
    # except:
    #     pass

    # if usertype == 'user':
    #     user = User.objects.create(
    #         username=username,
    #         password=password,
    #     )
    #     patient = Patient.objects.create(
    #         user=user,
    #         ssn=ssn,
    #     )
    #     login(request, user)
    # elif usertype == 'expert':
    #     pass
    # elif usertype == 'org':
    #     pass
    # messages.error(request, 'Invalid user type')
    # return redirect('cas')
