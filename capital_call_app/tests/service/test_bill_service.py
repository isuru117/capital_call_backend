from datetime import date
from django.test import SimpleTestCase
from unittest.mock import patch, MagicMock
from capital_call_app.enums.bill_type import BillType
from capital_call_app.services.bill_service import BillService
from capital_call_app.models.investor import Investor


class BillServiceTest(SimpleTestCase):

    def setUp(self):
        self.investor = Investor(
            id=1,
            name="John Doe",
            total_investment=20000,
            investment_date=date(2020, 10, 1)
        )

    @patch('capital_call_app.util.billing_util.calculate_membership_fee')
    @patch('capital_call_app.models.bill.Bill')
    def test_create_membership_fee(self, MockBill, mock_calculate_membership_fee):
        mock_calculate_membership_fee.return_value = 3000
        mock_bill_instance = MagicMock()
        MockBill.return_value = mock_bill_instance

        bill = BillService.create_membership_fee(self.investor)

        self.assertIsNotNone(bill)
        self.assertEqual(bill.amount, 3000)
        self.assertEqual(bill.bill_type, BillType.MEMBERSHIP)
        self.assertEqual(bill.investor, self.investor)

    @patch('capital_call_app.services.bill_service.calculate_membership_fee')
    def test_create_membership_fee_returns_none_if_fee_zero(self, mock_calculate_membership_fee):
        mock_calculate_membership_fee.return_value = 0
        bill = BillService.create_membership_fee(self.investor)

        self.assertIsNone(bill)

    @patch('capital_call_app.services.bill_service.calculate_upfront_fee')
    @patch('capital_call_app.models.bill.Bill')
    def test_create_upfront_fee(self, MockBill, mock_calculate_upfront_fee):
        mock_calculate_upfront_fee.return_value = 300
        mock_bill_instance = MagicMock()
        MockBill.return_value = mock_bill_instance

        bill = BillService.create_upfront_fee(self.investor)

        self.assertIsNotNone(bill)
        self.assertEqual(bill.amount, 300)
        self.assertEqual(bill.bill_type, BillType.UPFRONT_FEE)
        self.assertEqual(bill.investor, self.investor)

    @patch('capital_call_app.services.bill_service.calculate_yearly_fee')
    @patch('capital_call_app.models.bill.Bill')
    def test_create_yearly_fee(self, MockBill, mock_calculate_yearly_fee):
        mock_calculate_yearly_fee.return_value = 200
        mock_bill_instance = MagicMock()
        MockBill.return_value = mock_bill_instance

        bill = BillService.create_yearly_fee(self.investor, self.investor.investment_date)

        self.assertIsNotNone(bill)
        self.assertEqual(bill.amount, 200)
        self.assertEqual(bill.bill_type, BillType.YEARLY_FEE)
        self.assertEqual(bill.investor, self.investor)

    @patch('capital_call_app.services.bill_service.calculate_yearly_fee')
    def test_create_yearly_fee_returns_none_if_fee_zero(self, mock_calculate_yearly_fee):
        mock_calculate_yearly_fee.return_value = 0
        bill = BillService.create_yearly_fee(self.investor, self.investor.investment_date)

        self.assertIsNone(bill)

    @patch('capital_call_app.services.bill_service.calculate_membership_fee')
    @patch('capital_call_app.services.bill_service.calculate_upfront_fee')
    @patch('capital_call_app.services.bill_service.calculate_yearly_fee')
    def test_calculate_fee(self, mock_calculate_yearly_fee, mock_calculate_upfront_fee, mock_calculate_membership_fee):
        mock_calculate_membership_fee.return_value = 3000
        mock_calculate_upfront_fee.return_value = 500
        mock_calculate_yearly_fee.return_value = 2000

        bill = MagicMock(investor=self.investor, bill_type=BillType.MEMBERSHIP)
        calculated_fee = BillService.calculate_fee(bill)
        self.assertEqual(calculated_fee, 3000)

        bill.bill_type = BillType.UPFRONT_FEE
        calculated_fee = BillService.calculate_fee(bill)
        self.assertEqual(calculated_fee, 500)

        bill.bill_type = BillType.YEARLY_FEE
        calculated_fee = BillService.calculate_fee(bill)
        self.assertEqual(calculated_fee, 2000)

    @patch('capital_call_app.models.bill.Bill.objects.filter')
    def test_get_bills_by_investor(self, mock_filter):
        mock_filter.return_value = [
            MagicMock(amount=100, bill_type=BillType.MEMBERSHIP),
            MagicMock(amount=200, bill_type=BillType.UPFRONT_FEE),
            MagicMock(amount=300, bill_type=BillType.YEARLY_FEE)
        ]

        bills = BillService.get_bills_by_investor(self.investor.id)

        self.assertEqual(len(bills), 3)
        self.assertEqual(bills[0].amount, 100)
        self.assertEqual(bills[1].amount, 200)
        self.assertEqual(bills[2].amount, 300)
