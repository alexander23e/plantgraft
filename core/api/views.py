from rest_framework.generics import ListAPIView

from core.api.serializers import SaleSerializers
from core.erp.choices import TYPE_SALE
from core.erp.models import Sale


class SaleListAPIView(ListAPIView):
    queryset = Sale.objects.exclude(type=TYPE_SALE[1][0]).order_by('date_joined')
    serializer_class = SaleSerializers
    authentication_classes = []
    permission_classes = []
