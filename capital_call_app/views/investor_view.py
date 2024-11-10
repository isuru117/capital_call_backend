from datetime import date
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from capital_call_app.services.bill_service import BillService
from capital_call_app.serializers.investor_serializer import InvestorSerializer
from capital_call_app.serializers.bill_serializer import BillSerializer
from capital_call_app.models.investor import Investor


class InvestorView(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Investor.objects.all()
    serializer_class = InvestorSerializer

    def create(self, request, *args, **kwargs):
        investor_serializer = InvestorSerializer(data=request.data)
        if investor_serializer.is_valid():
            investor = investor_serializer.save()

            # Generate related bills using BillService
            bills = []

            # 1. Membership fee
            membership_bill = BillService.create_membership_fee(investor)
            if membership_bill:
                membership_bill.save()
                bills.append(membership_bill)

            # 2. Upfront fee
            upfront_bill = BillService.create_upfront_fee(investor)
            upfront_bill.save()
            bills.append(upfront_bill)

            # 3. Yearly fee
            investment_date = request.data.get('investment_date')
            if investment_date:
                investment_date = date.fromisoformat(investment_date)
                yearly_bill = BillService.create_yearly_fee(
                    investor, investment_date)

                # Create yearly bill if there is any to be accounted
                if yearly_bill != None:
                    yearly_bill.save()
                    bills.append(yearly_bill)

            # Return the response with the created investor and bills
            return Response(investor_serializer.data, status=status.HTTP_201_CREATED)

        return Response(investor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
