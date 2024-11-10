from django.db import models
from capital_call_app.models.capital_call import CapitalCall
from capital_call_app.models.investor import Investor
from capital_call_app.enums.bill_type import BillType


class Bill(models.Model):
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE)
    capital_call = models.ForeignKey(
        CapitalCall, on_delete=models.CASCADE, related_name='bills', null=True, blank=True
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bill_type = models.CharField(max_length=15, choices=BillType.choices)
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_bill_type_display()} Bill for {self.investor.name}"
