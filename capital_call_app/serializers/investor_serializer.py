import re
from rest_framework import serializers
from capital_call_app.models.investor import Investor


class InvestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investor
        fields = '__all__'
        
    def validate(self, data):
        # Basic IBAN regex
        iban_regex = r"^[A-Z]{2}\d{2}[A-Z0-9]{1,30}$"
        data['iban'] = data['iban'].replace(' ','').upper()
        if not re.match(iban_regex, data['iban']):
            raise serializers.ValidationError("Invalid IBAN format.")
        return data