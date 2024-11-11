from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from capital_call_app.serializers.bill_create_serializer import BillCreateSerializer
from capital_call_app.serializers.bill_serializer import BillSerializer
from capital_call_app.models.bill import Bill
from capital_call_app.services.bill_service import BillService


class BillView(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer

    @action(detail=False, methods=["get"], url_path="by-investor/(?P<investor_id>[^/.]+)")
    def get_bills_by_investor(self, request, investor_id=None):
        bills = BillService.get_bills_by_investor(investor_id=investor_id)
        
        # No bills generated for the investor yet
        if not bills.exists():
            return Response([], status=status.HTTP_200_OK)

        serializer = self.get_serializer(bills, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = BillCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            validated_data = serializer.validated_data
            bill_type = validated_data['bill_type']
            investor = validated_data['investor']
            
            amount = BillService.calculate_fee(Bill(bill_type=bill_type, investor=investor))
            
            bill = serializer.save(amount=amount)
            
            return Response(BillSerializer(bill).data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
