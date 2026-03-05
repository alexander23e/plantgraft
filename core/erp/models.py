import base64
import math
from datetime import datetime

from PIL import Image
from django.db import models
from django.db.models import Q, Sum, FloatField
from django.db.models.functions import Coalesce
from django.forms import model_to_dict

from config import settings
from core.erp.choices import CALCULATION_METHOD, TYPE_HEADINGS, MONTHS, TYPE_PRODUCT, TYPE_SALE, SALE_STATUS, STAGE_STATUS
from core.user.models import User


class Company(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre')
    ruc = models.CharField(max_length=13, verbose_name='RUC')
    address = models.CharField(max_length=200, verbose_name='Dirección')
    mobile = models.CharField(max_length=10, verbose_name='Teléfono celular')
    phone = models.CharField(max_length=9, verbose_name='Teléfono convencional')
    email = models.CharField(max_length=50, verbose_name='Email')
    website = models.CharField(max_length=250, verbose_name='Página web')
    description = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')
    mission = models.CharField(max_length=500, null=True, blank=True, verbose_name='Misión')
    vision = models.CharField(max_length=500, null=True, blank=True, verbose_name='Visión')
    about_us = models.CharField(max_length=500, null=True, blank=True, verbose_name='Acerca de nosotros')
    image = models.ImageField(null=True, blank=True, upload_to='company/%Y/%m/%d', verbose_name='Logo')
    iva = models.DecimalField(default=0.00, decimal_places=2, max_digits=9, verbose_name='IVA')
    latitude = models.CharField(max_length=30, verbose_name='Latitud')
    longitude = models.CharField(max_length=30, verbose_name='Longitud')
    email_host = models.CharField(max_length=30, default='smtp.gmail.com', verbose_name='Servidor de correo')
    email_port = models.IntegerField(default=587, verbose_name='Puerto del servidor de correo')
    email_host_user = models.CharField(max_length=100, verbose_name='Username del servidor de correo')
    email_host_password = models.CharField(max_length=30, verbose_name='Password del servidor de correo')

    def __str__(self):
        return self.name

    def get_image(self):
        if self.image:
            return f'{settings.MEDIA_URL}{self.image}'
        return f'{settings.STATIC_URL}img/default/empty.png'

    def get_full_path_image(self):
        if self.image:
            return self.image.path
        return f'{settings.BASE_DIR}{settings.STATIC_URL}img/default/empty.png'

    def get_iva(self):
        return float(self.iva)

    def get_image_in_base64(self):
        try:
            if self.image:
                src = self.image.path
                file = base64.b64encode(open(src, 'rb').read()).decode('utf-8')
                type = Image.open(src).format.lower()
                return f"data:image/{type};base64,{file}"
        except:
            pass
        return ''

    def toJSON(self):
        item = model_to_dict(self)
        item['image'] = self.get_image()
        item['iva'] = self.get_iva()
        item['image_in_base64'] = self.get_image_in_base64()
        return item

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        default_permissions = ()
        permissions = (
            ('view_company', 'Can view Empresa'),
        )
        ordering = ['-id']


class Headings(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name='Nombre')
    type = models.CharField(max_length=50, choices=TYPE_HEADINGS, default=TYPE_HEADINGS[0][0], verbose_name='Tipo')
    calculation_method = models.CharField(max_length=50, choices=CALCULATION_METHOD, default=CALCULATION_METHOD[0][0], verbose_name='Método de cálculo')
    percent = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Porcentaje')
    valor = models.FloatField(default=0.00, verbose_name='Valor')
    state = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return self.name

    def get_number(self):
        return f'{self.id:06d}'

    def toJSON(self):
        item = model_to_dict(self)
        item['calculation_method'] = {'id': self.calculation_method, 'name': self.get_calculation_method_display()}
        item['type'] = {'id': self.type, 'name': self.get_type_display()}
        item['percent'] = float(self.percent)
        return item

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        try:
            if self.calculation_method == CALCULATION_METHOD[0][0]:
                self.valor = self.percent / 100
            elif self.calculation_method == CALCULATION_METHOD[2][0]:
                self.valor = self.percent
        except:
            pass
        super(Headings, self).save()

    class Meta:
        verbose_name = 'Rubro'
        verbose_name_plural = 'Rubros'
        ordering = ['-id']


class Employee(models.Model):
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha de registro')
    names = models.CharField(max_length=150, verbose_name='Nombres')
    dni = models.CharField(max_length=10, unique=True, verbose_name='Número de cedula')
    mobile = models.CharField(max_length=10, unique=True, verbose_name='Teléfono')
    email = models.CharField(max_length=50, unique=True, verbose_name='Correo electrónico')
    address = models.CharField(max_length=500, null=True, blank=True, verbose_name='Dirección')
    rmu = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Salario mensual')
    headings = models.ManyToManyField(Headings, verbose_name='Rubros')
    state = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f'{self.names} ({self.dni})'

    def toJSON(self):
        item = model_to_dict(self)
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['rmu'] = float(self.rmu)
        item['headings'] = [i.toJSON() for i in self.headings.all()]
        return item

    def calculate_headings(self, rmu, type):
        valor = 0.00
        for i in self.headings.filter(state=True, type=type):
            if i.calculation_method == CALCULATION_METHOD[0][0]:
                valor += float(rmu) * i.valor
        return float(round(valor, 2))

    def calculate_headings_updated_salary(self, year, month, rmu, type):
        valor = 0.00
        salary_queryset = self.salary_set.filter(year=year, month=month)
        if salary_queryset.exists():
            salary = salary_queryset[0]
            for i in salary.salarydetail_set.filter(headings__type=type):
                valor += float(i.total)
        else:
            valor = self.calculate_headings(rmu=rmu, type=type)
        return valor

    def get_number(self):
        return f'{self.id:06d}'

    def salary_by_day(self):
        return self.rmu / 24

    def count_worked_days(self, year, month):
        return self.assistance_set.filter(date_joined__year=year, date_joined__month=month, state=True).count()

    def get_discount_loan(self):
        queryset = self.loans_set.filter(state=True)
        if queryset.exists():
            return float(queryset[0].role_discount)
        return 0.00

    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
        ordering = ['-id']


class Assistance(models.Model):
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha de asistencia')
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, verbose_name='Empleado')
    details = models.CharField(max_length=500, default='Sin detalles')
    state = models.BooleanField(default=False)

    def __str__(self):
        return self.details

    def toJSON(self):
        item = model_to_dict(self)
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['employee'] = self.employee.toJSON()
        return item

    class Meta:
        verbose_name = 'Asistencia'
        verbose_name_plural = 'Asistencias'
        ordering = ['id']


class Salary(models.Model):
    date_joined = models.DateField(default=datetime.now)
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
    year = models.IntegerField()
    month = models.IntegerField(choices=MONTHS, default=0)
    days_work = models.IntegerField(default=0)
    salary_by_day = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    rmu_contract = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    rmu_month = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    ingress = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    egress = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    discounts = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    loan_discount = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return self.employee.names

    def toJSON(self):
        item = model_to_dict(self)
        item['month'] = f'0{self.month}' if self.month < 10 else self.month
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['employee'] = self.employee.toJSON()
        item['rmu_contract'] = float(self.rmu_contract)
        item['rmu_month'] = float(self.rmu_month)
        item['salary_by_day'] = float(self.salary_by_day)
        item['ingress'] = float(self.ingress)
        item['egress'] = float(self.egress)
        item['discounts'] = float(self.discounts)
        item['loan_discount'] = float(self.loan_discount)
        item['total'] = float(self.total)
        return item

    def get_ingress(self):
        return self.salarydetail_set.filter(headings__type=TYPE_HEADINGS[0][0]).filter(Q(valor__gt=0.00) | Q(total__gt=0.00))

    def get_egress(self):
        return self.salarydetail_set.filter(headings__type=TYPE_HEADINGS[1][0]).filter(Q(valor__gt=0.00) | Q(total__gt=0.00))

    class Meta:
        verbose_name = 'Salario'
        verbose_name_plural = 'Salarios'
        ordering = ['-id']


class SalaryDetail(models.Model):
    salary = models.ForeignKey(Salary, on_delete=models.CASCADE)
    headings = models.ForeignKey(Headings, on_delete=models.PROTECT, null=True, blank=True)
    valor = models.FloatField(default=0.00)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return str(self.id)

    def get_heading_name(self):
        if self.headings.calculation_method in [CALCULATION_METHOD[0][0], CALCULATION_METHOD[2][0]]:
            return f'{self.headings.name} ({self.headings.valor})'
        return self.headings.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['salary'])
        item['heading_name'] = self.get_heading_name()
        item['headings'] = {} if self.headings is None else self.headings.toJSON()
        item['valor'] = self.valor
        item['total'] = float(self.total)
        return item

    class Meta:
        verbose_name = 'Salario Detalle'
        verbose_name_plural = 'Salarios Detalles'
        default_permissions = ()
        ordering = ['-id']


class Loans(models.Model):
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha de registro')
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, verbose_name='Empleado')
    valor = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Monto')
    saldo = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Saldo')
    quota = models.IntegerField(default=1, verbose_name='Coutas')
    role_discount = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Valor del descuento del Rol')
    state = models.BooleanField(default=False, verbose_name='Estado')

    def __str__(self):
        return self.employee.names

    def recalculate_debt(self):
        saldo = self.loanpayments_set.aggregate(result=Coalesce(Sum('valor'), 0.00, output_field=FloatField())).get('result')
        self.saldo = float(self.valor) - float(saldo)
        self.save()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.pk is None:
            self.saldo = self.valor
            self.role_discount = float(self.valor) / self.quota
        self.state = self.saldo > 0
        super(Loans, self).save()

    def toJSON(self):
        item = model_to_dict(self)
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['employee'] = self.employee.toJSON()
        item['valor'] = float(self.valor)
        item['role_discount'] = float(self.role_discount)
        item['saldo'] = float(self.saldo)
        return item

    class Meta:
        verbose_name = 'Prestamo'
        verbose_name_plural = 'Prestamos'
        ordering = ['id']


class LoanPayments(models.Model):
    loans = models.ForeignKey(Loans, on_delete=models.PROTECT)
    salary = models.ForeignKey(Salary, on_delete=models.PROTECT)
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha de registro')
    valor = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Valor')

    def __str__(self):
        return self.salary.employee.names

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(LoanPayments, self).save()
        amount = self.loans.loanpayments_set.aggregate(result=Coalesce(Sum('valor'), 0.00, output_field=FloatField())).get('result')
        self.loans.saldo = float(self.loans.valor) - amount
        self.loans.save()

    def delete(self, using=None, keep_parents=False):
        loans = self.loans
        super(LoanPayments, self).delete()
        loans.recalculate_debt()

    def toJSON(self):
        item = model_to_dict(self, exclude=['loans'])
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['salary'] = self.salary.toJSON()
        item['valor'] = float(self.valor)
        return item

    class Meta:
        verbose_name = 'Pago de Prestamo'
        verbose_name_plural = 'Pago de Prestamos'
        default_permissions = ()
        ordering = ['id']


class Client(models.Model):
    creation_date = models.DateField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=10, unique=True, verbose_name='Teléfono')
    birthdate = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento')
    address = models.CharField(max_length=500, null=True, blank=True, verbose_name='Dirección')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return self.user.get_full_name()

    def birthdate_format(self):
        return self.birthdate.strftime('%Y-%m-%d')

    def toJSON(self):
        item = model_to_dict(self)
        item['creation_date'] = self.creation_date.strftime('%Y-%m-%d')
        item['full_name'] = self.get_full_name()
        item['user'] = self.user.toJSON()
        item['birthdate'] = self.birthdate.strftime('%Y-%m-%d')
        return item

    def delete(self, using=None, keep_parents=False):
        super(Client, self).delete()
        try:
            self.user.delete()
        except:
            pass

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['-id']


class Provider(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Nombre')
    ruc = models.CharField(max_length=13, unique=True, verbose_name='RUC')
    mobile = models.CharField(max_length=10, unique=True, verbose_name='Teléfono celular')
    address = models.CharField(max_length=500, verbose_name='Dirección')
    email = models.CharField(max_length=50, unique=True, verbose_name='Email')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f'{self.name} ({self.ruc})'

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['-id']


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Nombre')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['-id']


class Resource(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre')
    code = models.CharField(max_length=8, unique=True, verbose_name='Código')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Categoría')
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Precio')
    image = models.ImageField(upload_to='resource/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f'{self.name} ({self.code}) ({self.category.name})'

    def get_short_name(self):
        return f'{self.name} ({self.category.name})'

    def get_or_create_category(self, name):
        category = Category()
        search = Category.objects.filter(name=name)
        if search.exists():
            category = search[0]
        else:
            category.name = name
            category.save()
        return category

    def toJSON(self):
        item = model_to_dict(self)
        item['full_name'] = self.get_full_name()
        item['short_name'] = self.get_short_name()
        item['category'] = self.category.toJSON()
        item['price'] = float(self.price)
        item['image'] = self.get_image()
        return item

    def get_image(self):
        if self.image:
            return f'{settings.MEDIA_URL}{self.image}'
        return f'{settings.STATIC_URL}img/default/empty.png'

    class Meta:
        verbose_name = 'Insumo'
        verbose_name_plural = 'Insumos'
        ordering = ['-name']


class Purchase(models.Model):
    number = models.CharField(max_length=8, unique=True, verbose_name='Número de factura')
    provider = models.ForeignKey(Provider, on_delete=models.PROTECT, verbose_name='Proveedor')
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha de registro')
    subtotal = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return self.provider.name

    def get_number(self):
        return f'{self.id:06d}'

    def calculate_invoice(self):
        subtotal = 0.00
        for i in self.purchasedetail_set.all():
            subtotal += float(i.price) * int(i.cant)
        self.subtotal = subtotal
        self.save()

    def delete(self, using=None, keep_parents=False):
        try:
            for i in self.purchasedetail_set.all():
                i.product.stock -= i.cant
                i.product.save()
                i.delete()
        except:
            pass
        super(Purchase, self).delete()

    def toJSON(self):
        item = model_to_dict(self)
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['provider'] = self.provider.toJSON()
        item['subtotal'] = float(self.subtotal)
        return item

    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'
        default_permissions = ()
        permissions = (
            ('view_purchase', 'Can view Compra'),
            ('add_purchase', 'Can add Compra'),
            ('delete_purchase', 'Can delete Compra'),
        )
        ordering = ['-id']


class PurchaseDetail(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.PROTECT)
    resource = models.ForeignKey(Resource, on_delete=models.PROTECT)
    cant = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    subtotal = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return self.resource.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['purchase'])
        item['resource'] = self.resource.toJSON()
        item['price'] = float(self.price)
        item['subtotal'] = float(self.subtotal)
        return item

    class Meta:
        verbose_name = 'Detalle de Compra'
        verbose_name_plural = 'Detalle de Compras'
        default_permissions = ()
        ordering = ['-id']


class Product(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Nombre')
    code = models.CharField(max_length=8, unique=True, verbose_name='Código')
    description = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')
    type = models.CharField(max_length=10, choices=TYPE_PRODUCT, default=TYPE_PRODUCT[0][0], verbose_name='Tipo')
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Precio')
    stock = models.IntegerField(default=0, verbose_name='Stock')
    image = models.ImageField(upload_to='product/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')

    def __str__(self):
        return self.name

    def get_price_promotion(self):
        promotions = self.promotionsdetail_set.filter(promotion__state=True)
        if promotions.exists():
            return promotions[0].price_final
        return 0.00

    def get_price_current(self):
        price_promotion = self.get_price_promotion()
        if price_promotion > 0:
            return price_promotion
        return self.price

    def get_image(self):
        if self.image:
            return f'{settings.MEDIA_URL}{self.image}'
        return f'{settings.STATIC_URL}img/default/empty.png'

    def get_short_name(self):
        return f'{self.name} ({self.get_type_display()})'

    def get_full_name(self):
        return f'{self.code} - {self.name} ({self.get_type_display()})'

    def toJSON(self):
        item = model_to_dict(self)
        item['full_name'] = self.get_full_name()
        item['short_name'] = self.get_short_name()
        item['price'] = float(self.price)
        item['image'] = self.get_image()
        item['price_promotion'] = float(self.get_price_promotion())
        item['price_current'] = float(self.get_price_current())
        item['type'] = {'id': self.type, 'name': self.get_type_display()}
        return item

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-id']


class Lot(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre')
    code = models.CharField(max_length=10, unique=True, verbose_name='Código')

    def __str__(self):
        return f'{self.name} ({self.code})'

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Lote'
        verbose_name_plural = 'Lotes'
        ordering = ['-id']


class Stage(models.Model):
    step = models.PositiveIntegerField(default=0, unique=True, verbose_name='Paso de la etapa')
    name = models.CharField(max_length=50, verbose_name='Nombre')
    color = models.CharField(max_length=50, verbose_name='Color')
    description = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')
    percent = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Porcentaje')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f'{self.step}.- {self.name} ({self.percent}%)'

    def toJSON(self):
        item = model_to_dict(self)
        item['text'] = self.get_full_name()
        item['full_name'] = self.get_full_name()
        item['percent'] = float(self.percent)
        return item

    class Meta:
        verbose_name = 'Etapa de Crecimiento'
        verbose_name_plural = 'Etapas de Crecimiento'
        ordering = ['id']


class Production(models.Model):
    start_date = models.DateField(default=datetime.now)
    end_date = models.DateField(default=datetime.now)
    lot = models.ForeignKey(Lot, on_delete=models.PROTECT, verbose_name='Lote')
    state = models.BooleanField(default=True)

    def __str__(self):
        return self.get_full_name()

    def get_state(self):
        if self.state:
            return 'Activa'
        return 'Finalizado'

    def get_full_name(self):
        term = f'{self.get_number()} / {self.lot.name} / {self.get_start_date()}'
        if not self.state:
            term += f'- {self.get_end_date()}'
        term += f' / {self.get_state()}'
        return term

    def get_short_name(self):
        return f'Producción: {self.get_number()} / Lote: {self.lot.name}'

    def get_number(self):
        return f'{self.id:06d}'

    def get_start_date(self):
        return self.start_date.strftime('%Y-%m-%d')

    def get_end_date(self):
        return self.end_date.strftime('%Y-%m-%d')

    def get_resources(self):
        return [i.toJSON() for i in self.productionresources_set.all()]

    def get_products(self):
        return [i.toJSON() for i in self.productionproducts_set.all()]

    def toJSON(self):
        item = model_to_dict(self)
        item['full_name'] = self.get_full_name()
        item['short_name'] = self.get_short_name()
        item['lot'] = self.lot.toJSON()
        item['number'] = self.get_number()
        item['start_date'] = self.get_start_date()
        item['end_date'] = self.get_end_date()
        return item

    def delete(self, using=None, keep_parents=False):
        for i in self.productionresources_set.all():
            i.resource.stock += i.cant
            i.save()
        super(Production, self).delete()

    class Meta:
        verbose_name = 'Producción'
        verbose_name_plural = 'Producciones'
        default_permissions = ()
        permissions = (
            ('view_production', 'Can view Producción'),
            ('add_production', 'Can add Producción'),
            ('delete_production', 'Can delete Producción'),
            ('view_harvest', 'Can view Cosecha'),
        )
        ordering = ['-id']


class ProductionResources(models.Model):
    production = models.ForeignKey(Production, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.PROTECT)
    cant = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    subtotal = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return self.resource.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['production'])
        item['resource'] = self.resource.toJSON()
        item['price'] = float(self.price)
        item['subtotal'] = float(self.subtotal)
        return item

    class Meta:
        verbose_name = 'Recurso de la Producción'
        verbose_name_plural = 'Recursos de la Producción'
        default_permissions = ()
        ordering = ['-id']


class ProductionProducts(models.Model):
    production = models.ForeignKey(Production, on_delete=models.CASCADE, verbose_name='Producción')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    cant = models.IntegerField(default=0)
    harvest_date = models.DateField(null=True, blank=True)
    loss = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    status = models.CharField(max_length=15, choices=STAGE_STATUS, default=STAGE_STATUS[0][0])

    def __str__(self):
        return self.product.name

    def validate_completed_stages(self):
        return not Stage.objects.filter().exclude(id__in=list(self.productionstages_set.filter().values_list('stage_id', flat=True))).exists()

    def get_current_stage(self):
        queryset_production_stages = self.productionstages_set.filter()
        if queryset_production_stages.exists():
            queryset_stage = Stage.objects.filter().exclude(id__in=list(queryset_production_stages.values_list('stage_id', flat=True))).order_by('step')
            if queryset_stage.exists():
                return queryset_stage[0]
            return queryset_production_stages.order_by('-stage__step')[0].stage
        return Stage.objects.filter().order_by('step')[0]

    def toJSON(self):
        item = model_to_dict(self, exclude=['production'])
        item['product'] = self.product.toJSON()
        item['harvest_date'] = '---' if self.harvest_date is None else self.harvest_date.strftime('%Y-%m-%d')
        item['status'] = {'id': self.status, 'name': self.get_status_display()}
        return item

    class Meta:
        verbose_name = 'Producto de la Producción'
        verbose_name_plural = 'Productos de la Producción'
        default_permissions = ()
        ordering = ['-id']


class ProductionStages(models.Model):
    production_products = models.ForeignKey(ProductionProducts, on_delete=models.CASCADE)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha de registro')
    observations = models.CharField(max_length=500, null=True, blank=True, verbose_name='Detalles')

    def __str__(self):
        return self.stage.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.observations is None:
            self.observations = 'Sin detalles'
        elif len(self.observations) == 0:
            self.observations = 'Sin detalles'
        super(ProductionStages, self).save()
        if self.production_products.validate_completed_stages():
            self.production_products.status = STAGE_STATUS[1][0]
            self.production_products.save()

    def toJSON(self):
        item = model_to_dict(self, exclude=['production'])
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['stage'] = self.stage.toJSON()
        return item

    class Meta:
        verbose_name = 'Etapa de Crecimiento de la Producción'
        verbose_name_plural = 'Etapa de Crecimiento de la Producción'
        default_permissions = ()
        permissions = (
            ('view_production_stages', 'Can view Etapa de Crecimiento de la Producción'),
        )
        ordering = ['-id']


class Promotions(models.Model):
    start_date = models.DateField(default=datetime.now)
    end_date = models.DateField(default=datetime.now)
    state = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)

    def toJSON(self):
        item = model_to_dict(self)
        item['start_date'] = self.start_date.strftime('%Y-%m-%d')
        item['end_date'] = self.end_date.strftime('%Y-%m-%d')
        return item

    class Meta:
        verbose_name = 'Promoción'
        verbose_name_plural = 'Promociones'
        ordering = ['-id']


class PromotionsDetail(models.Model):
    promotion = models.ForeignKey(Promotions, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    price_current = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    dscto = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    total_dscto = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    price_final = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return self.product.name

    def get_dscto_real(self):
        total_dscto = float(self.price_current) * float(self.dscto)
        n = 2
        return math.floor(total_dscto * 10 ** n) / 10 ** n

    def toJSON(self):
        item = model_to_dict(self, exclude=['promotion'])
        item['product'] = self.product.toJSON()
        item['price_current'] = float(self.price_current)
        item['dscto'] = float(self.dscto)
        item['total_dscto'] = float(self.total_dscto)
        item['price_final'] = float(self.price_final)
        return item

    class Meta:
        verbose_name = 'Detalle Promoción'
        verbose_name_plural = 'Detalle de Promociones'
        default_permissions = ()
        ordering = ['-id']


class Sale(models.Model):
    number = models.CharField(max_length=9, verbose_name='Número de comprobante')
    voucher = models.ImageField(upload_to='sale_voucher/%Y/%m/%d', null=True, blank=True, verbose_name='Comprobante')
    client = models.ForeignKey(Client, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Cliente')
    employee = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Empleado')
    type = models.CharField(max_length=10, choices=TYPE_SALE, default=TYPE_SALE[0][0], verbose_name='Tipo de Venta')
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha de registro')
    subtotal = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Subtotal')
    iva = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Iva')
    total_iva = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Valor de iva')
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Total a pagar')
    status = models.CharField(max_length=20, choices=SALE_STATUS, default=SALE_STATUS[0][0], verbose_name='Estado')
    paid = models.BooleanField(default=False, verbose_name='Pagado')

    def __str__(self):
        return self.get_full_name()

    def set_status(self):
        if self.type == TYPE_SALE[0][0]:
            self.status = SALE_STATUS[0][0]
        elif self.type == TYPE_SALE[1][0]:
            self.status = SALE_STATUS[2][0]
        elif self.type == TYPE_SALE[2][0]:
            self.status = SALE_STATUS[1][0]

    def get_voucher(self):
        if self.voucher:
            return f'{settings.MEDIA_URL}{self.voucher}'
        return f'{settings.STATIC_URL}img/default/empty.png'

    def get_iva_percent(self):
        return self.iva * 100

    def get_full_name(self):
        return f'{self.get_number()} / {self.client.user.names}'

    def generate_invoice_number(self):
        return f'{self.id:06d}'

    def get_number(self):
        return f'{self.id:06d}'

    def check_available_stock_of_products(self):
        response = {}
        products = []
        for i in self.saledetail_set.all():
            if i.product.stock < i.cant:
                products.append(i.product.get_short_name())
        if len(products):
            message = 'Los siguientes productos no cuentan con suficiente stock para poder despachar el pedido.<br>'
            for count, value in enumerate(products):
                message += f'{count + 1}). {value}<br>'
            response = {'error': message}
        return response

    def dispatch_products(self):
        for i in self.saledetail_set.all():
            i.product.stock -= i.cant
            i.product.save()
        self.status = SALE_STATUS[0][0]
        self.save()

    def date_joined_format(self):
        return self.date_joined.strftime('%Y-%m-%d')

    def toJSON(self):
        item = model_to_dict(self)
        item['full_name'] = self.get_full_name()
        item['number'] = self.get_number()
        item['voucher'] = self.get_voucher()
        item['type'] = {'id': self.type, 'name': self.get_type_display()}
        item['date_joined'] = self.date_joined_format()
        item['employee'] = {} if self.employee is None else self.client.toJSON()
        item['client'] = self.client.toJSON()
        item['subtotal'] = float(self.subtotal)
        item['iva'] = float(self.iva)
        item['total_iva'] = float(self.total_iva)
        item['total'] = float(self.total)
        item['status'] = {'id': self.status, 'name': self.get_status_display()}
        return item

    def calculate_invoice(self):
        subtotal = 0.00
        for i in self.saledetail_set.filter():
            i.subtotal = float(i.price) * int(i.cant)
            i.save()
            subtotal += i.subtotal
        self.subtotal = subtotal
        self.total_iva = self.subtotal * float(self.iva)
        self.total = float(self.subtotal) + float(self.total_iva)
        self.save()

    def delete(self, using=None, keep_parents=False):
        for detail in self.saledetail_set.filter(sale__paid=True).exclude(sale__type=TYPE_SALE[1][0]):
            detail.product.stock += detail.cant
            detail.product.save()
        super(Sale, self).delete()

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        default_permissions = ()
        permissions = (
            ('view_sale', 'Can view Venta'),
            ('add_sale', 'Can add Venta'),
            ('delete_sale', 'Can delete Venta'),
            ('view_sale_client', 'Can view Venta | Cliente'),
            ('add_sale_client', 'Can add Venta | Cliente'),
        )
        ordering = ['-id']


class SaleDetail(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    cant = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    subtotal = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return self.product.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['sale'])
        item['product'] = self.product.toJSON()
        item['price'] = float(self.price)
        item['subtotal'] = float(self.subtotal)
        return item

    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalle de Ventas'
        default_permissions = ()
        ordering = ['-id']
