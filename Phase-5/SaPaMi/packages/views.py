from django.shortcuts import render

from .models import TherapeuticPackage, Reservation, TherapeuticService, ServiceRecord, Bill, HealthExpert


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
        bill=bill
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
