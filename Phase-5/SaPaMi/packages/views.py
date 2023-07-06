from django.shortcuts import render

from .models import TherapeuticPackage, Reservation, TherapeuticService, ServiceRecord
from base.models import HealthExpert
from payment.models import Bill


def more_info(request, id):
    return render(request, 'packages/more_info.html', {'package': TherapeuticPackage.objects.get(id=id)})


def new_reservation(user):
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


def reserve_package(request, id):
    package = TherapeuticPackage.objects.get(id=id)
    date = request.POST.get('date')
    user = request.user
    reservation = Reservation.objects.filter(user=user).order_by('id').last()
    if reservation is None or reservation.status != Reservation.Status.PENDING:
        reservation = new_reservation(user)
    service = TherapeuticService.objects.create(
        reservation=reservation,
        therapeutic_package=package,
        datetime=date
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
    return render(request, 'packages/reserve_package.html', {'package': package})


def user_reservations(request):
    user = request.user
    reservations = Reservation.objects.filter(user=user)
    return render(request, 'packages/reservations.html', {'reservations': reservations})


def user_reservation(request, id):
    reservation = Reservation.objects.get(id=id)
    user = request.user
    if reservation.user.user.username != user.username:
        raise Exception('User is not authorized to view this reservation')
    services = TherapeuticService.objects.filter(reservation=reservation)
    return render(request, 'packages/reservation.html', {'reservation': reservation, 'services': services})
