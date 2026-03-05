import calendar
import json
import os
import random
import string
from tempfile import NamedTemporaryFile

import django
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from bs4 import BeautifulSoup
from django.core.files import File
from core.erp.models import *
from core.homepage.models import *
from core.security.models import *

numbers = list(string.digits)
letters = list(string.ascii_letters)
alphanumeric = numbers + letters


def     insert_data_json():
    company = Company()
    company.name = 'LEON ROSES'
    company.ruc = f"0{''.join(random.choices(numbers, k=12))}"
    company.email = 'leonroses@hotmail.com'
    company.phone = '2750263'
    company.mobile = f"0{''.join(random.choices(numbers, k=9))}"
    company.description = 'Nosotros nos dedicamos a la producción y comercialización de plantas ornamentales, árboles nativos y frutales. Prestamos servicio de paisajismo y suministro de insumos, brindamos asesoría y capacitación.'
    company.website = 'https://viverosdavid.com'
    company.address = 'Isidoro Guachamin Oe4-07 y, Quito 170301'
    company.mission = 'Somos una empresa dedicada a la producción y comercialización de plantas ornamentales, árboles nativos y frutales. Prestamos servicio de paisajismo y suministro de insumos, brindamos asesoría y capacitación. '
    company.vision = 'Liderar la producción de plantas frutales a nivel nacional, elevar los estándares de calidad y aumentar la competitividad de la fruticultura chilena a través de la investigación e innovación.'
    company.about_us = 'Somos una empresa que ha avanzando acorde a las necesidades del mercado frutícola, buscando mejorar y perfeccionar día a día la cadena de procesos del ciclo de propagación de plantas, para finalmente entregar plantas con un potencial productivo superior.'
    company.iva = 12.00
    company.save()

    SocialNetworks(url='https://twitter.com/', icon='fa-brands  fa-twitter', code='twitter').save()
    SocialNetworks(url='https://facebook.com/', icon='fa-brands  fa-facebook', code='facebook').save()
    SocialNetworks(url='https://instagram.com/', icon='fa-brands  fa-instagram', code='instagram').save()
    SocialNetworks(url='https://linkedin.com/', icon='fa-brands  fa-linkedin', code='linkedin').save()

    Testimonials(names='Jose Grasso', profession='Ingeniero Agrónomo', comment='En el último año, en el engorde hemos conseguido, con 100 días de estadía, un valor promedio de ganancia media diaria (GMD) de 914 gramos y una conversión alimenticia de 2,54 kilos de alimento por kilo de carne.').save()
    Testimonials(names='James Bongioanni', profession='Ingeniero de Alimentos', comment='Es una responsabilidad encarar grandes proyectos y que estos tengan cimientos sólidos. Y no sólo hablo de la estructura, también el respeto de la palabra, los plazos, y poder así cumplir a socios e inversores.').save()
    Testimonials(names='Jorge Menéndez', profession='Ingeniero Comercial', comment='Es por ello que creemos necesario trabajar con estaciones electrónicas de alimentación, este sistema nos permite dar a cada cerda el tipo de alimento que le corresponde y la cantidad del mismo en función de su condición corporal.').save()
    Testimonials(names='Gabriela Guamán', profession='Ingeniera de Biotecnología', comment='Cuando empezamos a pensar este proyecto, como visión de futuro, inversión y agregado de valor a la carne porcina, dudábamos si existía en el país un desarrollista de primer nivel.').save()
    Testimonials(names='Fátima Vargas', profession='Contadora', comment='Siempre hemos podido contar con ellos para cualquier reforma, ampliación o nuevas inversiones.').save()

    Services(name='Diseño y Decoración de Áreas Verdes', description='El diseño de espacios verdes nos permite intervenir sobre áreas urbanas sin connotación específica, re-inventarlas y convertirlas para que sean nuevamente útiles para nuestros clientes.').save()
    Services(name='Mantenimiento de Áreas Verdes', description='Es importante tener un mantenimiento continuo para conservar las áreas verdes en óptimas condiciones, generando así un ambiente armónico para nuestros clientes.').save()
    Services(name='Zona de siembra', description='Normalmente ubicada en un almacén, es donde se realiza la operación de sembrado mediante maquinaria automatizada o a mano. La siembra puede ser mediante el uso de semillas o por propagación vegetativa, normalmente a partir de estacas de ramas, esquejes').save()
    Services(name='Zonas de aclimatación', description='Se trata de una superficie cuya finalidad es la de preparar las plántulas para las condiciones de campo a las que se verán sometidas. Puede realizarse en el mismo invernadero de producción o en invernaderos de malla adyacentes a este.').save()
    Services(name='Sistemas de Riego', description='Enmarcados en el cuidado del medio ambiente y en asociación con la marca líder del mercado mundial en sistemas de riego nos permitimos diseñarlos y ejecutarlos de forma óptima y eficiente lo cual generan un ahorro en el consumo de agua para las áreas verdes.').save()

    FrequentQuestions(question='¿Que hay que tener en cuenta antes de comprar una planta?',
                      answer='En primer lugar, que la planta esté bien identificada para poder localizar todo lo necesario sobre sus cuidados y mantenimiento. Hay que asegurarse también de que contamos con las condiciones adecuadas para su correcto desarrollo en nuestro entorno.También es conveniente elegir las plantas con más flores, con las hojas sanas, y descartar directamente aquellas que tengan manchas sospechosas en tallos u hojas.').save()
    FrequentQuestions(question='¿Es conveniente llevarse del vivero una planta en maceta con las raices muy largas?',
                      answer='En un principio no. Si las raíces de la planta son demasiado largas y salen a través de los orificios de la maceta, habría que transplantarla cuanto antes, lo que puede ser perjudicial para la planta al unirse al cambio de ambiente consecuencia del traslado.').save()
    FrequentQuestions(question='¿Está bien una planta con musgo en la tierra?',
                      answer='Lo más conveniente es evitar este tipo de plantas, ya que el musgo localizado sobre la tierra es probablemente la consecuencia de un exceso de agua, lo que podría llegar a traducirse en unas raíces estropeadas o podridas.').save()
    FrequentQuestions(question='¿Es mejor una maceta de plástico o una de barro?',
                      answer='Sin duda la de plástico. Una maceta de plástico es más ligera, duradera y económica que otra de barro. Además, las macetas de barro, al ser porosas, retienen peor la humedad y es necesario regarlas con más frecuencia.').save()
    FrequentQuestions(question='¿Qué tamaño es el más adecuado para la maceta?',
                      answer='El tamaño más adecuado es el justo, ni más ni menos. No es muy conveniente que la maceta sea demasiado grande, sin embargo, las plantas de terraza necesitan recipientes algo más grandes mientras que las de plantas de interior es conveniente tenerlas en macetas más pequeñas.').save()
    FrequentQuestions(question='¿Qué plantas voy a poder cultivar en macetas?',
                      answer='Se pueden tener en maceta todas las plantas anuales y aquellas que sean de crecimiento lento y además deben resistir bien la sequía. También son adecuadas para cultivar en macetas todas las plantas que proceden de climas cálidos y deben ser protegidas en el invierno trasladándolas al invernadero o al interior de la casa.').save()

    Lot(name='Lote 1', code=''.join(random.choices(numbers, k=10))).save()
    Lot(name='Lote 2', code=''.join(random.choices(numbers, k=10))).save()
    Lot(name='Lote 3', code=''.join(random.choices(numbers, k=10))).save()
    Lot(name='Lote 4', code=''.join(random.choices(numbers, k=10))).save()

    Headings(name='IESS', type=TYPE_HEADINGS[0][0], calculation_method=CALCULATION_METHOD[0][0], percent=9.35, valor=0.0935, state=True).save()
    Headings(name='SEGURO MEDICO', type=TYPE_HEADINGS[0][0], calculation_method=CALCULATION_METHOD[0][0], percent=2.50, valor=0.025, state=True).save()
    Headings(name='ALIMENTACIÓN', type=TYPE_HEADINGS[0][0], calculation_method=CALCULATION_METHOD[2][0], percent=0.00, valor=1.30, state=True).save()
    Headings(name='HORAS EXTRA', type=TYPE_HEADINGS[1][0], calculation_method=CALCULATION_METHOD[1][0], percent=0.00, valor=0.00, state=True).save()

    Stage(step=1, percent=10, color='#E90000', name='Germinación', description='La semilla tiene las condiciones adecuadas (calor, agua y aire) se rompe y le brota una pequeña raíz. ').save()
    Stage(step=2, percent=25, color='#0F009C', name='Plántula', description='Cuando tu planta se convierta en una plántula, notarás que desarrolla más hojas de abanico tradicionales. ').save()
    Stage(step=3, percent=75, color='#076B0C', name='Vegetativa', description='Es donde realmente despega el crecimiento de la planta. En este punto, ha trasplantado su planta a una maceta más grande y las raíces y el follaje se están desarrollando rápidamente. Este también es el momento de comenzar a cubrir o entrenar sus plantas.').save()
    Stage(step=4, percent=100, color='#AC07B4', name='Floración', description='La etapa de floración es la etapa final de crecimiento de una planta. Aquí es cuando las plantas comienzan a desarrollar cogollos resinosos y tu arduo trabajo se hará realidad.').save()

    with open(f'{settings.BASE_DIR}/deploy/json/customers.json', encoding='utf8') as json_file:
        data = json.load(json_file)
        for item in data[0:10]:
            user = User()
            user.names = f"{item['first']} {item['last']}"
            user.dni = f"0{''.join(random.choices(numbers, k=9))}"
            user.email = item['email']
            user.username = user.dni
            user.set_password(user.dni)
            user.save()
            user.groups.add(Group.objects.get(pk=settings.GROUPS.get('client')))
            client = Client()
            client.user = user
            client.birthdate = date(random.randint(1969, 2006), random.randint(1, 12), random.randint(1, 28))
            client.mobile = f"0{''.join(random.choices(numbers, k=9))}"
            client.address = item['country']
            client.save()
        for item in data[11:20]:
            provider = Provider()
            provider.name = item['company'].upper()
            provider.ruc = f"0{''.join(random.choices(numbers, k=12))}"
            provider.mobile = f"0{''.join(random.choices(numbers, k=9))}"
            provider.address = item['country']
            provider.email = item['email']
            provider.save()
        for item in data[21:24]:
            employee = Employee()
            employee.names = f"{item['first']} {item['last']}"
            employee.dni = f"0{''.join(random.choices(numbers, k=9))}"
            employee.mobile = f"0{''.join(random.choices(numbers, k=9))}"
            employee.address = item['country']
            employee.email = item['email']
            employee.rmu = random.randint(425, 800)
            employee.save()
            for h in Headings.objects.all():
                employee.headings.add(h)

    current_date = datetime.now().date()
    monthrange = list(calendar.monthrange(current_date.year, current_date.month))[-1]

    for employee in Employee.objects.all():
        for day in range(1, monthrange):
            assistance = Assistance()
            assistance.employee = employee
            assistance.date_joined = datetime(2022, datetime.now().date().month, day)
            assistance.state = random.randint(0, 1) == 1
            assistance.save()

    with open(f'{settings.BASE_DIR}/deploy/json/products.json', encoding='utf8') as json_file:
        data = json.load(json_file)
        for i in data['rows'][0:80]:
            row = i['value']
            resource = Resource()
            resource.name = row['nombre']
            resource.code = ''.join(random.choices(alphanumeric, k=8)).upper()
            resource.category = resource.get_or_create_category(name=row['marca'])
            resource.price = random.randint(1, 10)
            resource.save()
            print(resource.name)

    for month in range(1, 13):
        customers = list(Client.objects.values_list('id', flat=True))
        for index in range(4, 8):
            date_joined = datetime.strptime(f'{2022}-{month}-{index}', '%Y-%m-%d')
            sale = Sale()
            sale.employee_id = 1
            sale.date_joined = date_joined
            sale.client_id = random.choice(customers)
            sale.iva = 0.12
            sale.paid = True
            sale.save()
            print(f'record inserted sale {sale.id}')
            for product in Product.objects.filter(stock__gt=0):
                detail = SaleDetail()
                detail.sale_id = sale.id
                detail.product_id = product.id
                max = int(product.stock * 0.03)
                if max == 0:
                    sale.delete()
                    break
                detail.cant = random.randint(1, max)
                detail.price = detail.product.price
                detail.save()
                detail.product.stock -= detail.cant
                detail.product.save()
            sale.calculate_invoice()
            sale.cash = sale.total
            sale.number = sale.get_number()
            sale.save()


# insert_data_json()

def get_products_scrapy():
    URL = 'https://excelag.com/productos/?lang=es'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    content_product = soup.select('div.portfolio')
    for item in content_product:
        category = item.select('div.column_attr h5')[0].text
        src = item.select('img.scale-with-grid')[0].get('src')
        name = item.select('div.column_attr p')[0].text
        response = requests.get(src, stream=True)
        if response.status_code != requests.codes.ok and len(name) == 0 and len(src) == 0 and len(category) == 0:
            continue
        with NamedTemporaryFile(delete=True) as file_temp:
            for chunk in response.iter_content(chunk_size=None):
                file_name = src.split('/')[-1]
                file_temp.write(chunk)
                resource = Resource()
                resource.name = name
                resource.code = ''.join(random.choices(alphanumeric, k=8)).upper()
                resource.category = resource.get_or_create_category(name=category)
                resource.price = random.randint(7, 30)
                resource.image.save(file_name, File(file_temp))
                resource.save()
                print(resource.id)
                break

# get_products_scrapy()
