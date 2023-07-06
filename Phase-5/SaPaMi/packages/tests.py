from django.test import TestCase

from base.models import Patient
from packages.models import TherapeuticPackage, Reservation, TherapeuticService
from packages.views import reserve_package
from django.test import RequestFactory

from model_bakery import baker
import datetime


class TestReservation(TestCase):
    def setUp(self):
        self.package = baker.make(TherapeuticPackage, approximate_price=1000)
        self.health_expert = baker.make('HealthExpert')
        self.user = baker.make('Patient')
        self.reservation_date = datetime.datetime(2020, 1, 1, 12, 0, 0)
        self.request = RequestFactory().post(f'/packages/{self.package.id}/reserve',
                                             {'date': self.reservation_date})
        self.request.user = self.user

    def check_reservation(self, reservation):
        self.assertIsNotNone(reservation)
        self.assertEqual(reservation.status, reservation.Status.PENDING)
        self.assertEqual(reservation.bill.total_cost, self.package.approximate_price)
        self.assertEqual(reservation.bill.total_paid, 0)
        self.assertEqual(reservation.health_expert, self.health_expert)
        service = TherapeuticService.objects.get(reservation=reservation)
        self.assertIsNotNone(service)
        self.assertEqual(service.therapeutic_package, self.package)
        self.assertEqual(service.datetime, datetime.datetime(2020, 1, 1, 12, 0, 0).astimezone())

    def test_new_reservation_should_be_made_for_new_user(self):
        reserve_package(self.request, self.package.id)
        self.assertEqual(Reservation.objects.count(), 1)
        reservation = Reservation.objects.get(user=self.user)
        self.check_reservation(reservation)

    def test_new_reservation_should_be_made_for_user_with_no_pending_reservations(self):
        baker.make('Reservation', user=self.user, status='C')
        reserve_package(self.request, self.package.id)
        self.assertEqual(Reservation.objects.count(), 2)
        reservation = Reservation.objects.filter(user=self.user).order_by('id').last()
        self.check_reservation(reservation)

    def test_new_reservation_should_not_be_made_for_user_with_pending_reservations(self):
        bill = baker.make('Bill', total_cost=0, total_paid=0)
        baker.make('Reservation', user=self.user, status='P', health_expert=self.health_expert, bill=bill)
        reserve_package(self.request, self.package.id)
        self.assertEqual(Reservation.objects.count(), 1)
        reservation = Reservation.objects.get(user=self.user)
        self.check_reservation(reservation)

    def test_new_reservation_should_not_be_made_if_no_health_expert_exists(self):
        self.health_expert.delete()
        with self.assertRaises(Exception):
            reserve_package(self.request, self.package.id)
        self.assertEqual(Reservation.objects.count(), 0)
