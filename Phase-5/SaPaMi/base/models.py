from django.db import models
from django.contrib.auth.models import User


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ssn = models.CharField(max_length=11, unique=True)
    last_login = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.user.username


class OrganizationUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.user.username


class HealthExpert(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254)
    experience = models.IntegerField()
    skype_id = models.CharField(max_length=100, blank=True)
    last_login = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.user.username


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


class HealthCenter(models.Model):
    class WorkField(models.TextChoices):
        PSYCHOLOGY = 'PS', 'Psychology'
        PSYCHIATRY = 'PY', 'Psychiatry'
        PSYCHOTHERAPY = 'PT', 'Psychotherapy'
        PSYCHOANALYSIS = 'PA', 'Psychoanalysis'

    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    work_fields = models.CharField(max_length=2, choices=WorkField.choices)
    center_license = models.ForeignKey(Document, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    medical_id = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    doctor_license = models.ForeignKey(Document, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
