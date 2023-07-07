from django.db import models

from base.models import Patient, HealthCenter, Doctor, HealthExpert
from payment.models import Bill


class Reservation(models.Model):
    class Status(models.TextChoices):
        PENDING = 'P', 'Pending'
        CANCELED = 'C', 'Canceled'
        FINISHED = 'F', 'Finished'
    user = models.ForeignKey(Patient, on_delete=models.CASCADE)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=Status.choices, default=Status.PENDING)
    health_expert = models.ForeignKey(HealthExpert, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.user.user.username


class TherapeuticPackage(models.Model):
    name = models.CharField(max_length=100)
    required_time = models.IntegerField()
    approximate_price = models.FloatField()
    prerequisites = models.TextField()
    health_center = models.ForeignKey(HealthCenter, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class TherapeuticPackageRating(models.Model):
    user = models.ForeignKey(Patient, on_delete=models.CASCADE)
    therapeutic_package = models.ForeignKey(TherapeuticPackage, on_delete=models.CASCADE)
    rating = models.FloatField()

    def __str__(self):
        return self.user.user.username + ' - ' + self.therapeutic_package.name


class Service(models.Model):
    reservation_date = models.DateField(auto_now_add=True)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)

    def __str__(self):
        return self.reservation.user.user.username + ' - ' + self.reservation_date.strftime('%Y-%m-%d')


class TherapeuticService(Service):
    therapeutic_package = models.ForeignKey(TherapeuticPackage, on_delete=models.CASCADE)
    datetime = models.DateTimeField()

    def __str__(self):
        return super().__str__() + ' - ' + self.therapeutic_package.name


class ServiceRecord(models.Model):
    class Status(models.TextChoices):
        PAID = 'P', 'Paid'
        PREPAID = 'R', 'Prepaid'
        UNPAID = 'U', 'Unpaid'

    service = models.OneToOneField(Service, on_delete=models.CASCADE)
    cost = models.FloatField()
    paid = models.FloatField()
    status = models.CharField(max_length=1, choices=Status.choices)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)

    def __str__(self):
        return self.service.__str__() + ' - ' + self.status
