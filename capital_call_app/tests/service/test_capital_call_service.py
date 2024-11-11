from django.test import SimpleTestCase
from unittest.mock import patch, MagicMock
from capital_call_app.services.capital_call_service import CapitalCallService
from capital_call_app.enums.status_choices import StatusChoices
from datetime import date, timedelta

class CapitalCallServiceTest(SimpleTestCase):

    @patch('capital_call_app.models.bill.Bill.objects.filter')
    @patch('capital_call_app.models.capital_call.CapitalCall.objects.create')
    def test_generate_capital_call(self, mock_capital_call_create, mock_bill_filter):
        mock_bill1 = MagicMock(amount=1000)
        mock_bill2 = MagicMock(amount=500)
        mock_bill_filter.return_value = [mock_bill1, mock_bill2]

        mock_capital_call = MagicMock()
        mock_capital_call_create.return_value = mock_capital_call

        capital_call = CapitalCallService.generate_capital_call([1, 2], investor=MagicMock())

        mock_bill_filter.assert_called_once_with(id__in=[1, 2])
        self.assertEqual(capital_call, mock_capital_call)

    @patch('capital_call_app.models.capital_call.CapitalCall.objects.filter')
    def test_get_capital_calls_by_investor(self, mock_capital_call_filter):

        mock_capital_call_filter.return_value = ["capital_call_1", "capital_call_2"]

        capital_calls = CapitalCallService.get_capital_calls_by_investor(1)

        mock_capital_call_filter.assert_called_once_with(investor_id=1)
        self.assertEqual(capital_calls, ["capital_call_1", "capital_call_2"])

    @patch('capital_call_app.models.capital_call.CapitalCall.objects.get')
    def test_update_capital_call(self, mock_capital_call_get):

        mock_capital_call = MagicMock()
        mock_capital_call_get.return_value = mock_capital_call


        new_status = StatusChoices.VALIDATED
        new_due_date = date.today() + timedelta(days=45)


        updated_capital_call = CapitalCallService.update_capital_call(
            capital_call_id=1, status=new_status, due_date=new_due_date
        )

        mock_capital_call_get.assert_called_once_with(id=1)
        mock_capital_call.save.assert_called_once()
        
        self.assertEqual(updated_capital_call.status, new_status)
        self.assertEqual(updated_capital_call.due_date, new_due_date)