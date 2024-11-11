from datetime import date
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from capital_call_app.serializers.investor_serializer import InvestorSerializer
from capital_call_app.models.investor import Investor
from capital_call_app.services.investor_service import InvestorService


class InvestorView(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Investor.objects.all()
    serializer_class = InvestorSerializer

    def create(self, request):
        investor_serializer = InvestorSerializer(data=request.data)
        if investor_serializer.is_valid():

            investor = InvestorService.create_investor_and_generate_bills(
                investor_serializer)

            response_serializer = InvestorSerializer(investor)

            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        return Response(investor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
