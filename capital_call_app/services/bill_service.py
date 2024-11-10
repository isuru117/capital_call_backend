from capital_call_app.models.bill import Bill
from capital_call_app.enums.bill_type import BillType
from capital_call_app.util.billing_util import calculate_membership_fee, calculate_upfront_fee, calculate_yearly_fee


class BillService:

    @staticmethod
    def create_membership_fee(investor):
        membership_fee = calculate_membership_fee(investor.total_investment)
        if membership_fee > 0:
            return Bill(
                investor=investor,
                amount=membership_fee,
                bill_type=BillType.MEMBERSHIP
            )
        return None

    @staticmethod
    def create_upfront_fee(investor):
        upfront_fee = calculate_upfront_fee(investor.total_investment)
        return Bill(
            investor=investor,
            amount=upfront_fee,
            bill_type=BillType.UPFRONT_FEE
        )

    @staticmethod
    def create_yearly_fee(investor, investment_date):
        yearly_fee = calculate_yearly_fee(
            investor.total_investment, investment_date)
        if yearly_fee == 0:
            return None
        return Bill(
            investor=investor,
            amount=yearly_fee,
            bill_type=BillType.YEARLY_FEE
        )

    @staticmethod
    def calculate_fee(bill):
        if bill.bill_type == BillType.MEMBERSHIP:
            return calculate_membership_fee(bill.investor.total_investment)
        if bill.bill_type == BillType.UPFRONT_FEE:
            return calculate_upfront_fee(bill.investor.total_investment)
        if bill.bill_type == BillType.YEARLY_FEE:
            return calculate_yearly_fee(bill.investor.total_investment,
                                        bill.investor.investment_date)

    @staticmethod
    def get_bills_by_investor(investor_id):
        bills = Bill.objects.filter(investor_id=investor_id)
        return bills
