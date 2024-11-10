from django.db import models


class Investor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    iban = models.CharField(max_length=34)
    total_investment = models.DecimalField(max_digits=15, decimal_places=2)
    investment_date = models.DateField()

    def __str__(self):
        return self.name
