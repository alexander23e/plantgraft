import os
import random
import string

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.security.models import *
from core.erp.models import *
from core.homepage.models import *
from django.contrib.auth.models import Permission
from core.user.models import User

numbers = list(string.digits)

dashboard = Dashboard()
dashboard.name = 'LEON ROSES'
dashboard.icon = 'fa-brands fa-pagelines'
dashboard.layout = 1
dashboard.navbar = 'navbar-dark navbar-navy'
dashboard.sidebar = 'sidebar-dark-navy'
dashboard.save()

moduletype = ModuleType()
moduletype.name = 'Seguridad'
moduletype.icon = 'fas fa-lock'
moduletype.save()
print(f'insertado {moduletype.name}')

module = Module()
module.module_type_id = 1
module.name = 'Tipos de Módulos'
module.url = '/security/module/type/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-door-open'
module.description = 'Permite administrar los tipos de módulos del sistema'
module.save()
for i in Permission.objects.filter(content_type__model=ModuleType._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 1
module.name = 'Módulos'
module.url = '/security/module/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-th-large'
module.description = 'Permite administrar los módulos del sistema'
module.save()
for i in Permission.objects.filter(content_type__model=Module._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 1
module.name = 'Grupos'
module.url = '/security/group/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-users'
module.description = 'Permite administrar los grupos de usuarios del sistema'
module.save()
for i in Permission.objects.filter(content_type__model=Group._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 1
module.name = 'Respaldos'
module.url = '/security/database/backups/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-database'
module.description = 'Permite administrar los respaldos de base de datos'
module.save()
for i in Permission.objects.filter(content_type__model=DatabaseBackups._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 1
module.name = 'Conf. Dashboard'
module.url = '/security/dashboard/update/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-tools'
module.description = 'Permite configurar los datos de la plantilla'
module.save()
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 1
module.name = 'Accesos'
module.url = '/security/access/users/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-user-secret'
module.description = 'Permite administrar los accesos de los usuarios'
module.save()
for i in Permission.objects.filter(content_type__model=AccessUsers._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 1
module.name = 'Usuarios'
module.url = '/user/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-user'
module.description = 'Permite administrar a los usuarios del sistema'
module.save()
for i in Permission.objects.filter(content_type__model=User._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

moduletype = ModuleType()
moduletype.name = 'Talento Humano'
moduletype.icon = 'fas fa-user-clock'
moduletype.save()
print(f'insertado {moduletype.name}')

module = Module()
module.module_type_id = 2
module.name = 'Rubros de Rol de pago'
module.url = '/erp/headings/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-file-invoice-dollar'
module.description = 'Permite administrar los rubros de los empleados'
module.save()
for i in Permission.objects.filter(content_type__model=Headings._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 2
module.name = 'Asistencias'
module.url = '/erp/assistance/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-calendar-check'
module.description = 'Permite administrar las asistencias de los empleados'
module.save()
for i in Permission.objects.filter(content_type__model=Assistance._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 2
module.name = 'Empleados'
module.url = '/erp/employee/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-user-tie'
module.description = 'Permite administrar los empleados del sistema'
module.save()
for i in Permission.objects.filter(content_type__model=Employee._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 2
module.name = 'Roles de Pago'
module.url = '/erp/salary/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-dollar-sign'
module.description = 'Permite administrar los roles de pago de los empleados'
module.save()
for i in Permission.objects.filter(content_type__model=Salary._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 2
module.name = 'Prestamos'
module.url = '/erp/loans/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fa-solid fa-sack-dollar'
module.description = 'Permite administrar los prestamos de los empleados'
module.save()
for i in Permission.objects.filter(content_type__model=Loans._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

moduletype = ModuleType()
moduletype.name = 'Inventario'
moduletype.icon = 'fas fa-boxes'
moduletype.save()
print(f'insertado {moduletype.name}')

module = Module()
module.module_type_id = 3
module.name = 'Proveedores'
module.url = '/erp/provider/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-truck'
module.description = 'Permite administrar a los proveedores de las compras'
module.save()
for i in Permission.objects.filter(content_type__model=Provider._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 3
module.name = 'Categorías'
module.url = '/erp/category/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-truck-loading'
module.description = 'Permite administrar las categorías de los productos'
module.save()
for i in Permission.objects.filter(content_type__model=Category._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 3
module.name = 'Insumos'
module.url = '/erp/resource/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-box'
module.description = 'Permite administrar los insumos del sistema'
module.save()
for i in Permission.objects.filter(content_type__model=Resource._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 3
module.name = 'Compras'
module.url = '/erp/purchase/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-dolly-flatbed'
module.description = 'Permite administrar las compras de los productos'
module.save()
for i in Permission.objects.filter(content_type__model=Purchase._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

moduletype = ModuleType()
moduletype.name = 'Facturación y Mark.'
moduletype.icon = 'fas fa-cart-arrow-down'
moduletype.save()
print(f'insertado {moduletype.name}')

module = Module()
module.module_type_id = 8
module.name = 'Ventas'
module.url = '/erp/sale/admin/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-shopping-cart'
module.description = 'Permite administrar las ventas de los productos'
module.save()
module.permits.add(Permission.objects.get(codename='view_sale'))
module.permits.add(Permission.objects.get(codename='add_sale'))
module.permits.add(Permission.objects.get(codename='delete_sale'))
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 4
module.name = 'Productos'
module.url = '/erp/product/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-box'
module.description = 'Permite administrar los productos del sistema'
module.save()
for i in Permission.objects.filter(content_type__model=Product._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 4
module.name = 'Compañia'
module.url = '/erp/company/update/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-building'
module.description = 'Permite administrar la información de la compañia'
module.save()
for i in Permission.objects.filter(content_type__model=Company._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 4
module.name = 'Clientes'
module.url = '/erp/client/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-user-check'
module.description = 'Permite administrar los clientes de la empresa'
module.save()
for i in Permission.objects.filter(content_type__model=Client._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.name = 'Ventas'
module.url = '/erp/sale/client/'
module.is_active = True
module.is_vertical = False
module.is_visible = True
module.icon = 'fas fa-shopping-cart'
module.description = 'Permite administrar las ventas de los productos'
module.save()
module.permits.add(Permission.objects.get(codename='view_sale_client'))
module.permits.add(Permission.objects.get(codename='add_sale_client'))
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 4
module.name = 'Promociones'
module.url = '/erp/promotions/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'far fa-calendar-check'
module.description = 'Permite administrar las promociones de los productos'
module.save()
for i in Permission.objects.filter(content_type__model=Promotions._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

moduletype = ModuleType()
moduletype.name = 'Gestión'
moduletype.icon = 'far fa-calendar-check'
moduletype.save()
print(f'insertado {moduletype.name}')

module = Module()
module.module_type_id = 5
module.name = 'Cosechas'
module.url = '/erp/harvest/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fa-solid fa-plate-wheat'
module.description = 'Permite administrar las cosechas de las plantas'
module.save()
module.permits.add(Permission.objects.get(codename='view_harvest'))
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 5
module.name = 'Producciones'
module.url = '/erp/production/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-calendar-check'
module.description = 'Permite administrar las producciones de las plantas e injertos'
module.save()
for i in Permission.objects.filter(content_type__model=Production._meta.label.split('.')[1].lower()).exclude(codename='view_harvest'):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 5
module.name = 'R.Crecimiento Plantas'
module.url = '/erp/production/stages/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fa-solid fa-book-bookmark'
module.description = 'Permite administrar el registro de crecimiento de las etapas de las plantas'
module.save()
for i in Permission.objects.filter(content_type__model=ProductionStages._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 5
module.name = 'Etapas de Crecimiento'
module.url = '/erp/stage/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-stopwatch'
module.description = 'Permite administrar las etapas de cosecha del cacao'
module.save()
for i in Permission.objects.filter(content_type__model=Stage._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 5
module.name = 'Lotes'
module.url = '/erp/lot/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fa-solid fa-earth-americas'
module.description = 'Permite administrar los lotes para las producciones'
module.save()
for i in Permission.objects.filter(content_type__model=Lot._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

moduletype = ModuleType()
moduletype.name = 'Página Principal'
moduletype.icon = 'fab fa-buffer'
moduletype.save()
print(f'insertado {moduletype.name}')

module = Module()
module.module_type_id = 6
module.name = 'Servicios'
module.url = '/services/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-broom'
module.description = 'Permite administrar los servicios de la compañia'
module.save()
for i in Permission.objects.filter(content_type__model=Services._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 6
module.name = 'Preguntas frecuentes'
module.url = '/frequent/questions/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-question-circle'
module.description = 'Permite administrar las preguntas frecuentes de la compañia'
module.save()
for i in Permission.objects.filter(content_type__model=FrequentQuestions._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 6
module.name = 'Redes Sociales'
module.url = '/social/networks/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-network-wired'
module.description = 'Permite administrar las redes sociales de la compañia'
module.save()
for i in Permission.objects.filter(content_type__model=SocialNetworks._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 6
module.name = 'Testimonios'
module.url = '/testimonials/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-comment-alt'
module.description = 'Permite administrar los testimonios de la compañia'
module.save()
for i in Permission.objects.filter(content_type__model=Testimonials._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

moduletype = ModuleType()
moduletype.name = 'Informes'
moduletype.icon = 'fas fa-chart-pie'
moduletype.save()
print(f'insertado {moduletype.name}')

module = Module()
module.module_type_id = 7
module.name = 'Proveedores'
module.url = '/reports/provider/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-bar'
module.description = 'Permite ver los reportes de los proveedores'
module.save()
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 7
module.name = 'Salarios'
module.url = '/reports/salary/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-bar'
module.description = 'Permite ver los reportes de los salarios de los empleados'
module.save()
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 7
module.name = 'Ventas'
module.url = '/reports/sale/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-bar'
module.description = 'Permite ver los reportes de las ventas'
module.save()
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 7
module.name = 'Resultados'
module.url = '/reports/results/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-bar'
module.description = 'Permite ver los reportes de perdidas y ganancias de la empresa'
module.save()
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 7
module.name = 'Productos'
module.url = '/reports/product/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-bar'
module.description = 'Permite ver los reportes de los productos'
module.save()
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 7
module.name = 'Producciones'
module.url = '/reports/production/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-bar'
module.description = 'Permite ver los reportes de las producciones'
module.save()
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 7
module.name = 'Ingresos/Egresos'
module.url = '/reports/inventory/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-bar'
module.description = 'Permite ver los reportes de los ingresos y egresos de las producciones de plantas'
module.save()
print(f'insertado {module.name}')

moduletype = ModuleType()
moduletype.name = 'BI'
moduletype.icon = 'far fa-chart-bar'
moduletype.save()
print(f'insertado {moduletype.name}')

module = Module()
module.module_type_id = 8
module.name = 'Ventas'
module.url = '/bi/sales/control/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-bar'
module.description = 'Permite ver los reportes el dashboard de bi de control de ventas'
module.save()
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 8
module.name = 'Ventas por Cliente'
module.url = '/bi/sales/per/customer/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-bar'
module.description = 'Permite ver los reportes el dashboard de bi de ventas por cliente'
module.save()
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 8
module.name = 'Productos'
module.url = '/bi/product/inquiries/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-bar'
module.description = 'Permite ver los reportes el dashboard de bi de productos'
module.save()
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 8
module.name = 'D.Clientes'
module.url = '/bi/customer/registered/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-bar'
module.description = 'Permite ver los reportes el dashboard de bi de clientes'
module.save()
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 8
module.name = 'D.Ingreso/Salida Prod.'
module.url = '/bi/products/inventory/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-bar'
module.description = 'Permite ver los reportes el dashboard de bi de ingreso y salida de productos'
module.save()
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 8
module.name = 'D.Precios de Prod.'
module.url = '/bi/products/prices/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-bar'
module.description = 'Permite ver los reportes el dashboard de bi de preecios de productos'
module.save()
print(f'insertado {module.name}')

module = Module()
module.name = 'Cambiar password'
module.url = '/user/update/password/'
module.is_active = True
module.is_vertical = False
module.is_visible = True
module.icon = 'fas fa-key'
module.description = 'Permite cambiar tu password de tu cuenta'
module.save()
print(f'insertado {module.name}')

module = Module()
module.name = 'Editar perfil'
module.url = '/user/update/profile/'
module.is_active = True
module.is_vertical = False
module.is_visible = True
module.icon = 'fas fa-user'
module.description = 'Permite cambiar la información de tu cuenta'
module.save()
print(f'insertado {module.name}')

group = Group()
group.name = 'Administrador'
group.save()
print(f'insertado {group.name}')

for m in Module.objects.filter().exclude(url__in=['/erp/sale/client/']):
    gm = GroupModule()
    gm.module = m
    gm.group = group
    gm.save()
    for p in m.permits.all():
        group.permissions.add(p)
        grouppermission = GroupPermission()
        grouppermission.module_id = m.id
        grouppermission.group_id = group.id
        grouppermission.permission_id = p.id
        grouppermission.save()

user = User()
user.names = 'William Jair Dávila Vargas'
user.username = 'admin'
user.dni = ''.join(random.choices(numbers, k=10))
user.email = 'davilawilliam93@gmail.com'
user.is_active = True
user.is_superuser = True
user.is_staff = True
user.set_password('hacker94')
user.save()
user.groups.add(group)
print(f'Bienvenido {user.names}')

group = Group()
group.name = 'Cliente'
group.save()
print(f'insertado {group.name}')

for m in Module.objects.filter(url__in=['/erp/sale/client/', '/user/update/profile/', '/user/update/password/']):
    gm = GroupModule()
    gm.module = m
    gm.group = group
    gm.save()
    for p in m.permits.all():
        group.permissions.add(p)
        grouppermission = GroupPermission()
        grouppermission.module_id = m.id
        grouppermission.group_id = group.id
        grouppermission.permission_id = p.id
        grouppermission.save()
