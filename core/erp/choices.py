CALCULATION_METHOD = (
    ('salary', 'Se calcula con el salario neto'),
    ('amount', 'Se ingresa una cantidad y valor'),
    ('value', 'Se calcula con un valor'),
)

TYPE_HEADINGS = (
    ('ingress', 'INGRESOS'),
    ('egress', 'EGRESOS'),
)

MONTHS = (
    ('', '-----------'),
    (1, 'Enero'),
    (2, 'Febrero'),
    (3, 'Marzo'),
    (4, 'Abril'),
    (5, 'Mayo'),
    (6, 'Junio'),
    (7, 'Julio'),
    (8, 'Agosto'),
    (9, 'Septiembre'),
    (10, 'Octubre'),
    (11, 'Noviembre'),
    (12, 'Diciembre')
)

TYPE_SALE = (
    ('sale', 'Venta'),
    ('quotation', 'Cotización'),
    ('order', 'Pedido'),
)

TYPE_PRODUCT = (
    ('plant', 'PLANTA'),
    ('graft', 'INJERTO'),
)

SALE_STATUS = (
    ('dispatched', 'Despachado'),
    ('awaiting_payment', 'En espera de pago'),
    ('quoted', 'Cotizado'),
)

STAGE_STATUS = (
    ('in_process', 'En Proceso'),
    ('finished', 'Por cosechar'),
    ('harvested', 'Cosechado'),
)

PRODUCT_OPTIONS = (
    ('best_seller', 'Mas vendido'),
    ('less_bought', 'Menos vendido'),
)
