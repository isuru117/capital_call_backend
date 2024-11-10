from datetime import date
from dateutil.relativedelta import relativedelta
from decimal import Decimal
from capital_call_app.enums.bill_type import BillType

FEE_PERCENTAGE=Decimal('0.02') # Applying an assumed a fixed fee percentage of 0.2% for calculations 
CUTOFF_DATE = date(2019, 4, 1) # Define the cutoff date for membership fees

def calculate_membership_fee(total_investment):
    # Free membership for high investments
    return Decimal(0) if total_investment > 50000 else Decimal(3000)


def calculate_upfront_fee(investment_amount):
    return FEE_PERCENTAGE * investment_amount * 5


def calculate_yearly_fee(investment_amount, investment_date):
    # Apply discount rates for subsequent years
    fee_percentage = FEE_PERCENTAGE
    
    # Calculate number of years since investment
    year = relativedelta(date.today(), investment_date).years

    # New investment without 1 year of completion
    if year == 0:
        return 0
    
    if investment_date < CUTOFF_DATE:
        if year == 1:
            days_in_year = 365 if investment_date.year % 4 != 0 else 366
            return (investment_date.timetuple().tm_yday / days_in_year) * fee_percentage * investment_amount
        else:
            return fee_percentage * investment_amount
    
    else:
        if year == 1:
            days_in_year = 365 if investment_date.year % 4 != 0 else 366
            return (investment_date.timetuple().tm_yday / days_in_year) * fee_percentage * investment_amount
        elif year == 2:
            return fee_percentage * investment_amount
        elif year == 3:
            return (fee_percentage - Decimal('0.002')) * investment_amount
        elif year == 4:
            return (fee_percentage - Decimal('0.005')) * investment_amount
        elif year >= 5:
            return (fee_percentage - Decimal('0.01')) * investment_amount
    