from django.test import TestCase

from packages.models import TherapeuticPackage, Reservation, TherapeuticService
from packages.views import reserve_package

from model_bakery import baker
import datetime


class TestReservation(TestCase):
    def setUp(self):
        self.package = baker.make(TherapeuticPackage, approximate_price=1000)
        self.health_expert = baker.make('HealthExpert')
        self.user = baker.make('Patient')
        self.client.force_login(self.user)

    def check_reservation(self, reservation):
        self.assertIsNotNone(reservation)
        self.assertEqual(reservation.status, reservation.Status.PENDING)
        self.assertEqual(reservation.bill.total_cost, self.package.approximate_price)
        self.assertEqual(reservation.bill.total_paid, 0)
        self.assertEqual(reservation.health_expert, self.health_expert)
        service = TherapeuticService.objects.get(reservation=reservation)
        self.assertIsNotNone(service)
        self.assertEqual(service.therapeutic_package, self.package)
        self.assertEqual(service.datetime, datetime.date.today().strftime('%Y-%m-%d'))

    def test_new_reservation_should_be_made_for_new_user(self):
        reserve_package(self.client, self.package.id)
        self.assertEqual(Reservation.objects.count(), 1)
        reservation = Reservation.objects.get(user=self.user)
        self.check_reservation(reservation)

    def test_new_reservation_should_be_made_for_user_with_no_pending_reservations(self):
        baker.make('Reservation', user=self.user, status='C')
        reserve_package(self.client, self.package.id)
        self.assertEqual(self.user.reservations.count(), 2)
        reservation = Reservation.objects.filter(user=self.user).order_by('id').last()
        self.check_reservation(reservation)

    def test_new_reservation_should_not_be_made_for_user_with_pending_reservations(self):
        baker.make('Reservation', user=self.user, status='P', health_expert=self.health_expert)
        reserve_package(self.client, self.package.id)
        self.assertEqual(Reservation.objects.count(), 1)
        reservation = Reservation.objects.get(user=self.user)
        self.check_reservation(reservation)

    def test_new_reservation_should_not_be_made_if_no_health_expert_exists(self):
        self.health_expert.delete()
        with self.assertRaises(Exception):
            reserve_package(self.client, self.package.id)
        self.assertEqual(Reservation.objects.count(), 0)
