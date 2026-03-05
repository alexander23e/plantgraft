from django.urls import path

from core.reports.views.inventory_report.views import InventoryReportView
from core.reports.views.production_report.views import ProductionReportView
from core.reports.views.provider_report.views import ProviderReportView
from core.reports.views.salary_report.views import SalaryReportView
from core.reports.views.sale_report.views import SaleReportView
from core.reports.views.results_report.views import ResultsReportView
from core.reports.views.product_report.views import ProductReportView

urlpatterns = [
    path('provider/', ProviderReportView.as_view(), name='provider_report'),
    path('salary/', SalaryReportView.as_view(), name='salary_report'),
    path('sale/', SaleReportView.as_view(), name='sale_report'),
    path('results/', ResultsReportView.as_view(), name='results_report'),
    path('product/', ProductReportView.as_view(), name='product_report'),
    path('production/', ProductionReportView.as_view(), name='production_report'),
    path('inventory/', InventoryReportView.as_view(), name='inventory_report'),
]
