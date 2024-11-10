from rest_framework import serializers
from capital_call_app.models.bill import Bill
from capital_call_app.models.capital_call import CapitalCall


class BillCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = ['bill_type', 'investor']
