from rest_framework import serializers
from capital_call_app.enums.status_choices import StatusChoices
from capital_call_app.models.capital_call import CapitalCall


class CapitalCallEditSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=StatusChoices.choices)
    due_date = serializers.DateField()

    def validate(self, data):
        capital_call_id = self.context.get("capital_call_id")
        if not CapitalCall.objects.filter(id=capital_call_id).exists():
            raise serializers.ValidationError(
                f"Capital Call with ID {capital_call_id} does not exist."
            )
        return data
