from capital_call_app.models.bill import Bill
from capital_call_app.models.capital_call import CapitalCall
from capital_call_app.enums.status_choices import StatusChoices
from datetime import timedelta, date

class CapitalCallService:

    @staticmethod
    def generate_capital_call(bill_ids, investor):
        # Retrieve bills from the database
        bills = Bill.objects.filter(id__in=bill_ids)
        if bills.count() != len(bill_ids):
            raise ValueError("One or more bills not found with the provided IDs.")

        # Calculate total amount
        total_amount = sum(bill.amount for bill in bills)

        # Create the CapitalCall
        capital_call = CapitalCall.objects.create(
            investor=investor,
            total_amount=total_amount,
            status=StatusChoices.VALIDATED,
            due_date=date.today() + timedelta(days=30)
        )

        # Link bills to the capital call
        for bill in bills:
            bill.capital_call = capital_call
            bill.save()

        return capital_call
    
    @staticmethod
    def get_capital_calls_by_investor(investor_id):
        capital_calls = CapitalCall.objects.filter(investor_id=investor_id)
        return capital_calls
    
    @staticmethod
    def update_capital_call(capital_call_id, status, due_date):
        capital_call = CapitalCall.objects.get(id=capital_call_id)
        capital_call.status = status
        capital_call.due_date = due_date
        capital_call.save()
        
        return capital_call