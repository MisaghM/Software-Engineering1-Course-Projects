from datetime import datetime

from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .models import TherapeuticPackage, Reservation, TherapeuticService, ServiceRecord
from base.models import HealthExpert, Patient
from payment.models import Bill


def more_info(request, id):
    return render(request, 'packages/more_info.html', {
        'package': TherapeuticPackage.objects.get(id=id),
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

    reservation = Reservation.objects.filter(user=user).order_by('id').last()
    if reservation is None or reservation.status != Reservation.Status.PENDING:
        reservation = new_reservation(user)
    service = TherapeuticService.objects.create(
        reservation=reservation,
        therapeutic_package=package,
        datetime=datetime.now()
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
    return redirect('confirm_reserve', id)


@login_required(login_url='cas')
def confirm_reserve(request, id):
    package = TherapeuticPackage.objects.get(id=id)
    if request.method == 'POST':
        reservation = Reservation.objects.filter(user=Patient.objects.get(user=request.user)).order_by('id').last()
        service = TherapeuticService.objects.filter(reservation=reservation, therapeutic_package=package).order_by('id').last()
        service_record = ServiceRecord.objects.get(service=service)
        service_record.paid = 0.3 * service_record.cost
        service_record.save()
        reservation.bill.total_paid += service_record.paid
        reservation.bill.save()
        return render(request, 'packages/reserve_thanks.html')
    return render(request, 'packages/confirm_reserve.html', {'package': package})


def user_reservations(request):
    user = Patient.objects.get(user=request.user)
    reservations = Reservation.objects.filter(user=user)
    return render(request, 'packages/reservations.html', {'reservations': reservations})


def user_reservation(request, id):
    reservation = Reservation.objects.get(id=id)
    if reservation.user.user.username != request.user.username:
        raise PermissionDenied
    services = TherapeuticService.objects.filter(reservation=reservation)
    return render(request, 'packages/reservation.html', {
        'reservation': reservation,
        'services': services
    })
