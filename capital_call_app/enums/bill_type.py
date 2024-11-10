from django.db import models

class BillType(models.TextChoices):
    MEMBERSHIP = 'membership', 'Membership'
    UPFRONT_FEE = 'upfront_fee', 'Upfront Fee'
    YEARLY_FEE = 'yearly_fee', 'Yearly Fee'