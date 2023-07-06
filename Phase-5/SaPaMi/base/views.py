from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET
from django.http import HttpResponseBadRequest
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, SignupForm, FilterForm
from .models import User, Patient
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


def cas(request):
    if request.user.is_authenticated:
        return redirect('home')
    lform = LoginForm()
    sform = SignupForm()

    if request.method == 'POST':
        type = request.POST.get('casType')
        if type == 'login':
            lform = LoginForm(data=request.POST)
            if lform.is_valid():
                user = lform.get_user()
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, 'Wrong username/password')
            else:
                if not User.objects.filter(username__iexact=lform.data['username']).exists():
                    messages.error(request, 'User does not exist')
                else:
                    messages.error(request, 'Wrong username/password')
        elif type == 'signup':
            sform = SignupForm(data=request.POST)
            if sform.is_valid():
                usertype = request.POST.get('usertype')
                ssn = request.POST.get('ssn')
                if None in (usertype, ssn):
                    return HttpResponseBadRequest()
                if not ssn.isdigit():
                    messages.error(request, 'SSN should be a number')
                    return redirect('cas')

                user = sform.save(commit=True)
                if usertype == 'user':
                    Patient.objects.create(
                        user=user,
                        ssn=ssn,
                    )
                elif usertype == 'expert':
                    pass
                elif usertype == 'org':
                    pass

                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Username already exists')
        else:
            return HttpResponseBadRequest()

    return render(request, 'base/cas.html', {
        'lform': lform,
        'sform': sform,
    })


@login_required(login_url='cas')
def cas_logout(request):
    logout(request)
    return redirect('home')
