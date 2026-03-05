from django.urls import path
from core.api.views import *

urlpatterns = [
    path('sale/list/', SaleListAPIView.as_view(), name='api_sale_list'),
]
