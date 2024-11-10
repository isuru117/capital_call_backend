from django.db import models
from capital_call_app.models.investor import Investor
from capital_call_app.enums.status_choices import StatusChoices


class CapitalCall(models.Model):
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=10, choices=StatusChoices.choices)
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Capital Call {self.pk} for {self.investor.name}"
