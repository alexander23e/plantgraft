from django.urls import path

from core.bi.views.client_bi.views import CustomerRegisteredIView
from core.bi.views.product_bi.views import ProductInquiriesBIView, ProductsInventoryBIView, ProductsPricesBIView
from core.bi.views.sale_bi.views import SalesControlBIView, SalesPerCustomerBIView

urlpatterns = [
    path('sales/control/', SalesControlBIView.as_view(), name='bi_sales_control'),
    path('sales/per/customer/', SalesPerCustomerBIView.as_view(), name='bi_sales_per_customer'),
    path('product/inquiries/', ProductInquiriesBIView.as_view(), name='bi_product_inquiries'),
    path('customer/registered/', CustomerRegisteredIView.as_view(), name='bi_customer_registered'),
    path('products/inventory/', ProductsInventoryBIView.as_view(), name='bi_products_inventory'),
    path('products/prices/', ProductsPricesBIView.as_view(), name='bi_products_prices'),
]
