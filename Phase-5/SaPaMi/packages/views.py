from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.core.exceptions import PermissionDenied
from django.db.models import Avg

from .models import TherapeuticPackage, Reservation, TherapeuticService, ServiceRecord, TherapeuticPackageRating
from base.models import HealthExpert, Patient
from payment.models import Bill


def more_info(request, id):
    package = TherapeuticPackage.objects.get(id=id)
    avg = TherapeuticPackageRating.objects.filter(therapeutic_package=package).aggregate(Avg('rating'))['rating__avg']

    rating = None
    if request.user.is_authenticated:
        user = Patient.objects.get(user=request.user)
        r = TherapeuticPackageRating.objects.filter(user=user, therapeutic_package=package).first()
        if r is not None:
            rating = r.rating
    return render(request, 'packages/more_info.html', {
        'package': package,
        'avg': avg,
        'rating': rating,
    })


def new_reservation(user: Patient):
    bill = Bill.objects.create(
        total_cost=0,
        total_paid=0
    )
    health_expert = HealthExpert.objects.order_by('?').first()
    if health_expert is None:
        raise Exception('No health expert exists')
    reservation = Reservation.objects.create(
        user=user,
        bill=bill,
        health_expert=health_expert
    )
    return reservation


@login_required(login_url='cas')
@require_POST
def reserve_package(request, id):
    package = TherapeuticPackage.objects.get(id=id)
    user = Patient.objects.get(user=request.user)
    date = request.POST.get('reserveDate')
    reservation = Reservation.objects.filter(user=user).order_by('id').last()
    if reservation is None or reservation.status != Reservation.Status.PENDING:
        reservation = new_reservation(user)
    service = TherapeuticService.objects.create(
        reservation=reservation,
        therapeutic_package=package,
        datetime=date,
    )
    ServiceRecord.objects.create(
        service=service,
        cost=package.approximate_price,
        paid=0,
        status=ServiceRecord.Status.UNPAID,
        bill=reservation.bill
    )
    reservation.bill.total_cost += package.approximate_price
    reservation.bill.save()
    return redirect('confirm_service', service.id)


@login_required(login_url='cas')
def confirm_service(request, id):
    service = TherapeuticService.objects.get(id=id)
    service_record = ServiceRecord.objects.get(service=service)
    package = service.therapeutic_package
    already_paid = service_record.status != ServiceRecord.Status.UNPAID
    if already_paid:
        return render(request, 'packages/reserve_thanks.html', {'already_paid': already_paid})
    if request.method == 'POST':
        user = Patient.objects.get(user=request.user)
        reservation = Reservation.objects.filter(user=user).order_by('id').last()
        service_record.paid = 0.3 * service_record.cost
        service_record.status = ServiceRecord.Status.PREPAID
        service_record.save()
        reservation.bill.total_paid += service_record.paid
        reservation.bill.save()
        return render(request, 'packages/reserve_thanks.html', {'already_paid': already_paid})
    return render(request, 'packages/confirm_service.html', {
        'package': package,
        'service': service,
    })


@login_required(login_url='cas')
@require_POST
def rate_package(request, id):
    package = TherapeuticPackage.objects.get(id=id)
    if not request.user.is_authenticated:
        return redirect('cas')
    try:
        rating = float(request.POST.get('rating'))
    except:
        return HttpResponseBadRequest()
    user = Patient.objects.get(user=request.user)
    rate = TherapeuticPackageRating.objects.filter(user=user, therapeutic_package=package).first()
    if rate is None:
        TherapeuticPackageRating.objects.create(
            user=user,
            therapeutic_package=package,
            rating=rating,
        )
    else:
        rate.rating = rating
        rate.save()
    return redirect('packages', id)


@login_required(login_url='cas')
def reservations(request):
    user = Patient.objects.get(user=request.user)
    reservations = Reservation.objects.filter(user=user)
    status = [Reservation.Status(x.status).label for x in reservations]
    return render(request, 'packages/reservations.html', {
        'reservations': zip(reservations, status),
    })


@login_required(login_url='cas')
def reservation(request, id):
    reservation = Reservation.objects.get(id=id)
    if reservation.user.user.username != request.user.username:
        raise PermissionDenied
    reservation_status = Reservation.Status(reservation.status).label

    services = TherapeuticService.objects.filter(reservation=reservation)
    service_records = []
    service_status = []
    for x in services:
        sr = ServiceRecord.objects.get(service=x)
        service_records.append(sr)
        service_status.append(ServiceRecord.Status(sr.status).label)

    return render(request, 'packages/reservation.html', {
        'reservation': reservation,
        'reservation_status': reservation_status,
        'services': zip(services, service_records, service_status),
    })
