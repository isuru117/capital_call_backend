from django.db import models

class StatusChoices(models.TextChoices):
    VALIDATED = 'validated', 'Validated'
    SENT = 'sent', 'Sent'
    PAID = 'paid', 'Paid'
    OVERDUE = 'overdue', 'Overdue'