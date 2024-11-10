from rest_framework import serializers
from capital_call_app.models.bill import Bill
from capital_call_app.models.capital_call import CapitalCall


class BillSerializer(serializers.ModelSerializer):
    capital_call = serializers.PrimaryKeyRelatedField(
        queryset=CapitalCall.objects.all(),
        allow_null=True,
        required=False
    )

    class Meta:
        model = Bill
        fields = '__all__'