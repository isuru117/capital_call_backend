from capital_call_app.models.investor import Investor
from capital_call_app.services.bill_service import BillService
from datetime import date


class InvestorService:

    @staticmethod
    def create_investor_and_generate_bills(investor_serializer):

            investor = investor_serializer.save()

            bills = []

            # 1. Membership fee
            membership_bill = BillService.create_membership_fee(investor)
            if membership_bill:
                membership_bill.save()
                bills.append(membership_bill)

            # 2. Upfront fee
            upfront_bill = BillService.create_upfront_fee(investor)
            upfront_bill.save()
            bills.append(upfront_bill)

            # 3. Yearly fee
            investment_date = investor.investment_date
            if investment_date:
                yearly_bill = BillService.create_yearly_fee(
                    investor, investment_date)

                # Create yearly bill if there is any to be accounted
                if yearly_bill is not None:
                    yearly_bill.save()
                    bills.append(yearly_bill)

            return investor

