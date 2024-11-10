from django.core.management.base import BaseCommand
from capital_call_app.models.bill import Bill
from capital_call_app.models.capital_call import CapitalCall
from capital_call_app.models.investor import Investor
from capital_call_app.enums.bill_type import BillType
from capital_call_app.enums.status_choices import StatusChoices
from decimal import Decimal
from datetime import date

class Command(BaseCommand):
    help = 'Pre-seed data into the Investor, CapitalCall, and Bill models.'

    def handle(self, *args, **options):
        # Seed Investors
        if not Investor.objects.exists():
            self.stdout.write('Seeding Investor data...')
            investor1 = Investor.objects.create(
                name='John Doe',
                email='john@example.com',
                iban='FR7630006000011234567890189',
                total_investment=Decimal('50000.00'),
                investment_date=date(2021, 1, 1)
            )
            investor2 = Investor.objects.create(
                name='Jane Smith',
                email='jane@example.com',
                iban='FR7630006000019876543210987',
                total_investment=Decimal('75000.00'),
                investment_date=date(2020, 5, 15)
            )
            self.stdout.write(self.style.SUCCESS('Investor data seeded successfully.'))
        else:
            self.stdout.write(self.style.WARNING('Investor data already exists.'))

        # Seed CapitalCalls
        if not CapitalCall.objects.exists():
            self.stdout.write('Seeding CapitalCall data...')
            capital_call1 = CapitalCall.objects.create(
                investor=investor1,
                total_amount=Decimal('10000.00'),
                status=StatusChoices.OVERDUE,
                due_date=date(2024, 12, 15)
            )
            capital_call2 = CapitalCall.objects.create(
                investor=investor2,
                total_amount=Decimal('15000.00'),
                status=StatusChoices.PAID,
                due_date=date(2023, 10, 10)
            )
            self.stdout.write(self.style.SUCCESS('CapitalCall data seeded successfully.'))
        else:
            self.stdout.write(self.style.WARNING('CapitalCall data already exists.'))

        # Seed Bills
        if not Bill.objects.exists():
            self.stdout.write('Seeding Bill data...')
            Bill.objects.create(
                investor=investor1,
                capital_call=capital_call1,
                amount=Decimal('2000.00'),
                bill_type=BillType.UPFRONT_FEE
            )
            Bill.objects.create(
                investor=investor1,
                capital_call=capital_call1,
                amount=Decimal('3000.00'),
                bill_type=BillType.MEMBERSHIP
            )
            Bill.objects.create(
                investor=investor2,
                capital_call=capital_call2,
                amount=Decimal('2500.00'),
                bill_type=BillType.YEARLY_FEE
            )
            self.stdout.write(self.style.SUCCESS('Bill data seeded successfully.'))
        else:
            self.stdout.write(self.style.WARNING('Bill data already exists.'))
