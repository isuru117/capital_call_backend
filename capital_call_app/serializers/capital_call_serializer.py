from rest_framework import serializers
from capital_call_app.serializers.bill_serializer import BillSerializer
from capital_call_app.models.capital_call import CapitalCall
from capital_call_app.serializers.investor_serializer import InvestorSerializer


class CapitalCallSerializer(serializers.ModelSerializer):
    bills = BillSerializer(many=True, read_only=True)
    investor = InvestorSerializer(read_only=True)

    class Meta:
        model = CapitalCall
        fields = '__all__'