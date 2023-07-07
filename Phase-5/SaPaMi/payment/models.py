from django.db import models
from django.contrib.auth.models import User


class Bill(models.Model):
    total_cost = models.FloatField()
    total_paid = models.FloatField()

    def __str__(self):
        return str(self.total_cost)


class Payment(models.Model):
    date = models.DateField()
    amount = models.FloatField()
    reference = models.CharField(max_length=100)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)

    def __str__(self):
        return self.reference


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
