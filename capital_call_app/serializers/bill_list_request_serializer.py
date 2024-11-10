from rest_framework import serializers
from capital_call_app.models.bill import Bill
from capital_call_app.models.investor import Investor


class BillListRequestSerializer(serializers.Serializer):
    bill_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
        help_text="A list of bill IDs to include in the capital call"
    )
    investor_id = serializers.IntegerField(
        help_text="The ID of the investor to whom the bills belong"
    )

    def validate_bill_ids(self, value):
        if not Bill.objects.filter(id__in=value).count() == len(value):
            raise serializers.ValidationError("One or more bills with the provided IDs do not exist.")
        return value
    
    def validate_investor_id(self, value):
        if not Investor.objects.filter(id=value).exists():
            raise serializers.ValidationError(f"Investor with ID {value} does not exist.")
        return value