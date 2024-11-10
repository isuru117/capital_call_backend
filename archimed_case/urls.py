from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularSwaggerView,SpectacularAPIView

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from capital_call_app.views.capital_call_view import CapitalCallView
from capital_call_app.views.bill_view import BillView
from capital_call_app.views.investor_view import InvestorView


router = DefaultRouter()
router.register(r'investors', InvestorView)
router.register(r'bills', BillView)
router.register(r'capital_calls', CapitalCallView)

urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('', include(router.urls)),
]