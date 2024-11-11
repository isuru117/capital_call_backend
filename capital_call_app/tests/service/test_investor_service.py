from unittest.mock import patch, MagicMock
from django.test import SimpleTestCase
from capital_call_app.services.investor_service import InvestorService


class InvestorServiceTest(SimpleTestCase):

    @patch('capital_call_app.services.bill_service.BillService.create_membership_fee')
    @patch('capital_call_app.services.bill_service.BillService.create_upfront_fee')
    @patch('capital_call_app.services.bill_service.BillService.create_yearly_fee')
    def test_create_investor_and_generate_bills(self, mock_create_yearly_fee, mock_create_upfront_fee, mock_create_membership_fee):
        mock_investor_serializer = MagicMock()
        mock_investor = MagicMock()
        mock_investor_serializer.save.return_value = mock_investor

        mock_membership_bill = MagicMock()
        mock_membership_bill.save = MagicMock()
        mock_create_membership_fee.return_value = mock_membership_bill

        mock_upfront_bill = MagicMock()
        mock_upfront_bill.save = MagicMock()
        mock_create_upfront_fee.return_value = mock_upfront_bill

        mock_yearly_bill = MagicMock()
        mock_yearly_bill.save = MagicMock()
        mock_create_yearly_fee.return_value = mock_yearly_bill

        investor = InvestorService.create_investor_and_generate_bills(
            mock_investor_serializer)

        mock_investor_serializer.save.assert_called_once()

        mock_create_membership_fee.assert_called_once_with(mock_investor)
        mock_create_upfront_fee.assert_called_once_with(mock_investor)
        mock_create_yearly_fee.assert_called_once_with(
            mock_investor, mock_investor.investment_date)

        mock_membership_bill.save.assert_called_once()
        mock_upfront_bill.save.assert_called_once()
        mock_yearly_bill.save.assert_called_once()

        self.assertEqual(investor, mock_investor)

    @patch('capital_call_app.services.bill_service.BillService.create_membership_fee')
    @patch('capital_call_app.services.bill_service.BillService.create_upfront_fee')
    @patch('capital_call_app.services.bill_service.BillService.create_yearly_fee')
    def test_create_investor_and_generate_bills_no_yearly_fee(self, mock_create_yearly_fee, mock_create_upfront_fee, mock_create_membership_fee):
        mock_investor_serializer = MagicMock()
        mock_investor = MagicMock()
        mock_investor_serializer.save.return_value = mock_investor

        mock_membership_bill = MagicMock()
        mock_membership_bill.save = MagicMock()
        mock_create_membership_fee.return_value = mock_membership_bill

        mock_upfront_bill = MagicMock()
        mock_upfront_bill.save = MagicMock()
        mock_create_upfront_fee.return_value = mock_upfront_bill

        mock_create_yearly_fee.return_value = None

        investor = InvestorService.create_investor_and_generate_bills(
            mock_investor_serializer)

        mock_investor_serializer.save.assert_called_once()

        mock_create_membership_fee.assert_called_once_with(mock_investor)
        mock_create_upfront_fee.assert_called_once_with(mock_investor)
        mock_create_yearly_fee.assert_called_once_with(
            mock_investor, mock_investor.investment_date)

        mock_membership_bill.save.assert_called_once()
        mock_upfront_bill.save.assert_called_once()

        self.assertEqual(investor, mock_investor)
