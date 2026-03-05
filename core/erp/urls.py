from django.urls import path

from core.erp.views.assistance.views import *
from core.erp.views.category.views import *
from core.erp.views.client.views import *
from core.erp.views.company.views import *
from core.erp.views.employee.views import *
from core.erp.views.harvest.views import *
from core.erp.views.headings.views import *
from core.erp.views.loans.views import *
from core.erp.views.lot.views import *
from core.erp.views.product.views import *
from core.erp.views.production.views import *
from core.erp.views.production_stages.views import *
from core.erp.views.promotions.views import *
from core.erp.views.provider.views import *
from core.erp.views.purchase.views import *
from core.erp.views.resource.views import *
from core.erp.views.salary.views import *
from core.erp.views.sale.views import *
from core.erp.views.stage.views import *

urlpatterns = [
    # company
    path('company/update/', CompanyUpdateView.as_view(), name='company_update'),
    # provider
    path('provider/', ProviderListView.as_view(), name='provider_list'),
    path('provider/add/', ProviderCreateView.as_view(), name='provider_create'),
    path('provider/update/<int:pk>/', ProviderUpdateView.as_view(), name='provider_update'),
    path('provider/delete/<int:pk>/', ProviderDeleteView.as_view(), name='provider_delete'),
    # client
    path('client/', ClientListView.as_view(), name='client_list'),
    path('client/add/', ClientCreateView.as_view(), name='client_create'),
    path('client/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    path('client/update/profile/', ClientUpdateProfileView.as_view(), name='client_update_profile'),
    # employee
    path('employee/', EmployeeListView.as_view(), name='employee_list'),
    path('employee/add/', EmployeeCreateView.as_view(), name='employee_create'),
    path('employee/update/<int:pk>/', EmployeeUpdateView.as_view(), name='employee_update'),
    path('employee/delete/<int:pk>/', EmployeeDeleteView.as_view(), name='employee_delete'),
    # headings
    path('headings/', HeadingsListView.as_view(), name='headings_list'),
    path('headings/add/', HeadingsCreateView.as_view(), name='headings_create'),
    path('headings/update/<int:pk>/', HeadingsUpdateView.as_view(), name='headings_update'),
    path('headings/delete/<int:pk>/', HeadingsDeleteView.as_view(), name='headings_delete'),
    # assistance
    path('assistance/', AssistanceListView.as_view(), name='assistance_list'),
    path('assistance/add/', AssistanceCreateView.as_view(), name='assistance_create'),
    path('assistance/update/<str:date_joined>/', AssistanceUpdateView.as_view(), name='assistance_create'),
    path('assistance/delete/<str:start_date>/<str:end_date>/', AssistanceDeleteView.as_view(), name='assistance_delete'),
    # salary
    path('salary/', SalaryListView.as_view(), name='salary_list'),
    path('salary/add/', SalaryCreateView.as_view(), name='salary_create'),
    path('salary/update/<int:year>/<int:month>/', SalaryUpdateView.as_view(), name='salary_update'),
    path('salary/delete/<int:year>/<int:month>/', SalaryDeleteView.as_view(), name='salary_delete'),
    path('salary/print/receipt/<int:pk>/', SalaryPrintReceiptView.as_view(), name='salary_print_receipt'),
    # loans
    path('loans/', LoansListView.as_view(), name='loans_list'),
    path('loans/add/', LoansCreateView.as_view(), name='loans_create'),
    path('loans/delete/<int:pk>/', LoansDeleteView.as_view(), name='loans_delete'),
    # provider
    path('provider/', ProviderListView.as_view(), name='provider_list'),
    path('provider/add/', ProviderCreateView.as_view(), name='provider_create'),
    path('provider/update/<int:pk>/', ProviderUpdateView.as_view(), name='provider_update'),
    path('provider/delete/<int:pk>/', ProviderDeleteView.as_view(), name='provider_delete'),
    # category
    path('category/', CategoryListView.as_view(), name='category_list'),
    path('category/add/', CategoryCreateView.as_view(), name='category_create'),
    path('category/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),
    # product
    path('product/', ProductListView.as_view(), name='product_list'),
    path('product/add/', ProductCreateView.as_view(), name='product_create'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    # product
    path('resource/', ResourceListView.as_view(), name='resource_list'),
    path('resource/add/', ResourceCreateView.as_view(), name='resource_create'),
    path('resource/update/<int:pk>/', ResourceUpdateView.as_view(), name='resource_update'),
    path('resource/delete/<int:pk>/', ResourceDeleteView.as_view(), name='resource_delete'),
    # purchase
    path('purchase/', PurchaseListView.as_view(), name='purchase_list'),
    path('purchase/add/', PurchaseCreateView.as_view(), name='purchase_create'),
    path('purchase/delete/<int:pk>/', PurchaseDeleteView.as_view(), name='purchase_delete'),
    # stage
    path('stage/', StageListView.as_view(), name='stage_list'),
    path('stage/add/', StageCreateView.as_view(), name='stage_create'),
    path('stage/update/<int:pk>/', StageUpdateView.as_view(), name='stage_update'),
    path('stage/delete/<int:pk>/', StageDeleteView.as_view(), name='stage_delete'),
    # lot
    path('lot/', LotListView.as_view(), name='lot_list'),
    path('lot/add/', LotCreateView.as_view(), name='lot_create'),
    path('lot/update/<int:pk>/', LotUpdateView.as_view(), name='lot_update'),
    path('lot/delete/<int:pk>/', LotDeleteView.as_view(), name='lot_delete'),
    # promotions
    path('promotions/', PromotionsListView.as_view(), name='promotions_list'),
    path('promotions/add/', PromotionsCreateView.as_view(), name='promotions_create'),
    path('promotions/update/<int:pk>/', PromotionsUpdateView.as_view(), name='promotions_update'),
    path('promotions/delete/<int:pk>/', PromotionsDeleteView.as_view(), name='promotions_delete'),
    # productions
    path('production/', ProductionListView.as_view(), name='production_list'),
    path('production/add/', ProductionCreateView.as_view(), name='production_create'),
    path('production/delete/<int:pk>/', ProductionDeleteView.as_view(), name='production_delete'),
    # production_stages
    path('production/stages/', ProductionStagesCreateView.as_view(), name='production_stages_create'),
    path('production/stages/<int:pk>/', ProductionStagesCreateView.as_view(), name='production_stages_create'),
    # harvest
    path('harvest/', HarvestCreateView.as_view(), name='harvest_create'),
    # sale
    path('sale/admin/', SaleListView.as_view(), name='sale_admin_list'),
    path('sale/admin/add/', SaleCreateView.as_view(), name='sale_admin_create'),
    path('sale/admin/delete/<int:pk>/', SaleDeleteView.as_view(), name='sale_admin_delete'),
    path('sale/admin/print/invoice/<int:pk>/', SalePrintInvoiceView.as_view(), name='sale_admin_print_invoice'),
    path('sale/client/', SaleClientListView.as_view(), name='sale_client_list'),
    path('sale/client/print/invoice/<int:pk>/', SalePrintInvoiceView.as_view(), name='sale_client_print_invoice'),
    path('sale/client/add/', SaleClientCreateView.as_view(), name='sale_client_create'),
]
