from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema
from capital_call_app.serializers.capital_call_edit_serializer import CapitalCallEditSerializer
from capital_call_app.services.capital_call_service import CapitalCallService
from capital_call_app.serializers.bill_list_request_serializer import BillListRequestSerializer
from capital_call_app.serializers.capital_call_serializer import CapitalCallSerializer
from capital_call_app.models.investor import Investor
from capital_call_app.models.capital_call import CapitalCall


class CapitalCallView(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = CapitalCall.objects.all()
    serializer_class = CapitalCallSerializer

    @extend_schema(
        request=BillListRequestSerializer,
        responses={201: CapitalCallSerializer},
    )
    @action(detail=False, methods=["post"])
    def generate(self, request):
        bill_ids = request.data.get("bill_ids", [])
        investor_id = request.data.get("investor_id")

        investor = get_object_or_404(Investor, id=investor_id)

        try:
            capital_call = CapitalCallService.generate_capital_call(
                bill_ids, investor)

            serializer = self.get_serializer(capital_call)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"], url_path="by-investor/(?P<investor_id>[^/.]+)")
    def get_capital_call_by_investor(self, request, investor_id=None):
        capital_calls = CapitalCallService.get_capital_calls_by_investor(
            investor_id=investor_id)
        if not capital_calls.exists():
            return Response({"detail": "No bills found for the given investor."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(capital_calls, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=CapitalCallEditSerializer,
        responses={200: CapitalCallSerializer},
    )
    @action(detail=True, methods=["patch"], url_path="update")
    def update_capital_call(self, request, pk=None):
        serializer = CapitalCallEditSerializer(
            data=request.data, context={"capital_call_id": pk}
        )

        if serializer.is_valid():
            new_status = serializer.validated_data["status"]
            new_due_date = serializer.validated_data["due_date"]

            try:
                updated_capital_call = CapitalCallService.update_capital_call(
                    pk, new_status, new_due_date)
                response_serializer = self.get_serializer(updated_capital_call)
                return Response(response_serializer.data, status=status.HTTP_200_OK)

            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
