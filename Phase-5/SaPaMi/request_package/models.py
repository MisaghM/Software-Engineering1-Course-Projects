from django.db import models
from django.contrib.auth.models import User


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ssn = models.CharField(max_length=11, unique=True)

    def __str__(self):
        return self.user.username


class OrganizationUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class HealthExpert(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254)
    experience = models.IntegerField()
    skype_id = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username


class CreditCard(models.Model):
    class Type(models.TextChoices):
        VISA = 'V', 'Visa'
        MASTERCARD = 'M', 'MasterCard'
        AMERICAN_EXPRESS = 'A', 'American Express'

    number = models.CharField(max_length=16)
    cvv2 = models.CharField(max_length=3)
    expiration_date = models.DateField()
    type = models.CharField(max_length=1, choices=Type.choices)
    holder_name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.number


class Document(models.Model):
    class Type(models.TextChoices):
        PATIENT_PREREQUISITES = 'PP', 'Patient Prerequisites'
        HEALTH_CENTER_LICENSE = 'HL', 'Health Center License'
        DOCTOR_LICENSE = 'DL', 'Doctor License'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=Type.choices)
    file = models.FileField(upload_to='documents/')
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username + ' - ' + self.type


class Bill(models.Model):
    total_cost = models.FloatField()
    total_paid = models.FloatField()

    def __str__(self):
        return self.total_cost


class Payment(models.Model):
    date = models.DateField()
    amount = models.FloatField()
    reference = models.CharField(max_length=100)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)

    def __str__(self):
        return self.reference


class Reservation(models.Model):
    user = models.ForeignKey(Patient, on_delete=models.CASCADE)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.user.username


class HealthCenter(models.Model):
    class WorkField(models.TextChoices):
        PSYCHOLOGY = 'PS', 'Psychology'
        PSYCHIATRY = 'PY', 'Psychiatry'
        PSYCHOTHERAPY = 'PT', 'Psychotherapy'
        PSYCHOANALYSIS = 'PA', 'Psychoanalysis'

    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    work_fields = models.CharField(max_length=2, choices=WorkField.choices)
    center_license = models.ForeignKey(Document, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    medical_id = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    doctor_license = models.ForeignKey(Document, on_delete=models.CASCADE)


class TherapeuticPackage(models.Model):
    name = models.CharField(max_length=100)
    required_time = models.IntegerField()
    approximate_price = models.FloatField()
    prerequisites = models.TextField()
    health_center = models.ForeignKey(HealthCenter, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Service(models.Model):
    reservation_date = models.DateField()
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)

    def __str__(self):
        return self.reservation.user.user.username + ' - ' + self.reservation_date


class TherapeuticService(Service):
    therapeutic_package = models.ForeignKey(TherapeuticPackage, on_delete=models.CASCADE)
    datetime = models.DateTimeField()

    def __str__(self):
        return super().__str__() + ' - ' + self.therapeutic_package.name


class ServiceRecord(models.Model):
    class Status(models.TextChoices):
        PAID = 'P', 'Paid'
        UNPAID = 'U', 'Unpaid'

    service = models.OneToOneField(Service, on_delete=models.CASCADE)
    cost = models.FloatField()
    paid = models.FloatField()
    status = models.CharField(max_length=1, choices=Status.choices)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
