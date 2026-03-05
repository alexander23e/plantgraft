var current_date;
var fvSale, fvClient;
var select_client;
var input_birthdate, input_search_products, input_date_joined;
var tblSearchProducts, tblProducts;

var sale = {
    details: {
        subtotal: 0.00,
        iva: 0.00,
        total_iva: 0.00,
        dscto: 0.00,
        total_dscto: 0.00,
        total: 0.00,
        cash: 0.00,
        change: 0.00,
        products: [],
    },
    calculateInvoice: function () {
        console.clear();
        this.details.subtotal = 0.00;
        this.details.products.forEach(function (value, index, array) {
            value.subtotal = value.price_current * value.cant;
            sale.details.subtotal += value.subtotal;
        });
        this.details.total_iva = this.details.subtotal * this.details.iva;
        this.details.total = sale.details.subtotal + sale.details.total_iva;
        this.details.total = parseFloat(sale.details.total.toFixed(2));

        $('input[name="subtotal"]').val(sale.details.subtotal.toFixed(2));
        $('input[name="iva"]').val(sale.details.iva.toFixed(2));
        $('input[name="total_iva"]').val(sale.details.total_iva.toFixed(2));
        $('input[name="total"]').val(sale.details.total.toFixed(2));
    },
    listProducts: function () {
        this.calculateInvoice();
        tblProducts = $('#tblProducts').DataTable({
            autoWidth: false,
            destroy: true,
            data: this.details.products,
            ordering: false,
            lengthChange: false,
            searching: false,
            paginate: false,
            columns: [
                {data: "id"},
                {data: "full_name"},
                {data: "stock"},
                {data: "cant"},
                {data: "price_current"},
                {data: "subtotal"},
            ],
            columnDefs: [
                {
                    targets: [-4],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<span class="badge badge-secondary badge-pill">'+data+'</span>';
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<input type="text" class="form-control" autocomplete="off" name="cant" value="' + row.cant + '">';
                    }
                },
                {
                    targets: [-1, -2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + data.toFixed(2);
                    }
                },
                {
                    targets: [0],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-flat btn-xs"><i class="fas fa-times"></i></a>';
                    }
                },
            ],
            rowCallback: function (row, data, index) {
                var tr = $(row).closest('tr');
                tr.find('input[name="cant"]')
                    .TouchSpin({
                        min: 1,
                        max: data.stock
                    })
                    .on('keypress', function (e) {
                        return validate_form_text('numbers', e, null);
                    });
            },
            initComplete: function (settings, json) {
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
    },
    getProductsIds: function () {
        return this.details.products.map(value => value.id);
    },
    addProduct: function (item) {
        this.details.products.push(item);
        this.listProducts();
    },
};

document.addEventListener('DOMContentLoaded', function (e) {
    fvClient = FormValidation.formValidation(document.getElementById('frmClient'), {
            locale: 'es_ES',
            localization: FormValidation.locales.es_ES,
            plugins: {
                trigger: new FormValidation.plugins.Trigger(),
                submitButton: new FormValidation.plugins.SubmitButton(),
                bootstrap: new FormValidation.plugins.Bootstrap(),
                icon: new FormValidation.plugins.Icon({
                    valid: 'fa fa-check',
                    invalid: 'fa fa-times',
                    validating: 'fa fa-refresh',
                }),
            },
            fields: {
                names: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
                        },
                    }
                },
                dni: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 10
                        },
                        digits: {},
                        remote: {
                            url: pathname,
                            data: function () {
                                return {
                                    parameter: fvClient.form.querySelector('[name="dni"]').value,
                                    pattern: 'dni',
                                    action: 'validate_client'
                                };
                            },
                            message: 'El número de cédula ya se encuentra registrado',
                            method: 'POST',
                            headers: {
                                'X-CSRFToken': csrftoken
                            },
                        }
                    }
                },
                mobile: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 7
                        },
                        digits: {},
                        remote: {
                            url: pathname,
                            data: function () {
                                return {
                                    parameter: fvClient.form.querySelector('[name="mobile"]').value,
                                    pattern: 'mobile',
                                    action: 'validate_client'
                                };
                            },
                            message: 'El número de teléfono ya se encuentra registrado',
                            method: 'POST',
                            headers: {
                                'X-CSRFToken': csrftoken
                            },
                        }
                    }
                },
                email: {
                    validators: {
                        // notEmpty: {},
                        stringLength: {
                            min: 5
                        },
                        regexp: {
                            regexp: /^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$/i,
                            message: 'El formato email no es correcto'
                        },
                        remote: {
                            url: pathname,
                            data: function () {
                                return {
                                    parameter: fvClient.form.querySelector('[name="email"]').value,
                                    pattern: 'email',
                                    action: 'validate_client'
                                };
                            },
                            message: 'El email ya se encuentra registrado',
                            method: 'POST',
                            headers: {
                                'X-CSRFToken': csrftoken
                            },
                        }
                    }
                },
                address: {
                    validators: {
                        stringLength: {
                            min: 4,
                        }
                    }
                },
                image: {
                    validators: {
                        file: {
                            extension: 'jpeg,jpg,png',
                            type: 'image/jpeg,image/png',
                            maxFiles: 1,
                            message: 'Introduce una imagen válida'
                        }
                    }
                },
                birthdate: {
                    validators: {
                        notEmpty: {
                            message: 'La fecha es obligatoria'
                        },
                        date: {
                            format: 'YYYY-MM-DD',
                            message: 'La fecha no es válida'
                        }
                    },
                },
            },
        }
    )
        .on('core.element.validated', function (e) {
            if (e.valid) {
                const groupEle = FormValidation.utils.closest(e.element, '.form-group');
                if (groupEle) {
                    FormValidation.utils.classSet(groupEle, {
                        'has-success': false,
                    });
                }
                FormValidation.utils.classSet(e.element, {
                    'is-valid': false,
                });
            }
            const iconPlugin = fvClient.getPlugin('icon');
            const iconElement = iconPlugin && iconPlugin.icons.has(e.element) ? iconPlugin.icons.get(e.element) : null;
            iconElement && (iconElement.style.display = 'none');
        })
        .on('core.validator.validated', function (e) {
            if (!e.result.valid) {
                const messages = [].slice.call(fvClient.form.querySelectorAll('[data-field="' + e.field + '"][data-validator]'));
                messages.forEach((messageEle) => {
                    const validator = messageEle.getAttribute('data-validator');
                    messageEle.style.display = validator === e.validator ? 'block' : 'none';
                });
            }
        })
        .on('core.form.valid', function () {
            var parameters = new FormData(fvClient.form);
            parameters.append('action', 'create_client');
            submit_formdata_with_ajax('Notificación', '¿Estas seguro de realizar la siguiente acción?', pathname,
                parameters,
                function (request) {
                    var newOption = new Option(request.user.names + ' / ' + request.user.dni, request.id, false, true);
                    select_client.append(newOption).trigger('change');
                    fvSale.revalidateField('client');
                    $('#myModalClient').modal('hide');
                }
            );
        });
});

document.addEventListener('DOMContentLoaded', function (e) {
    fvSale = FormValidation.formValidation(document.getElementById('frmSale'), {
            locale: 'es_ES',
            localization: FormValidation.locales.es_ES,
            plugins: {
                trigger: new FormValidation.plugins.Trigger(),
                submitButton: new FormValidation.plugins.SubmitButton(),
                bootstrap: new FormValidation.plugins.Bootstrap(),
                // excluded: new FormValidation.plugins.Excluded(),
                icon: new FormValidation.plugins.Icon({
                    valid: 'fa fa-check',
                    invalid: 'fa fa-times',
                    validating: 'fa fa-refresh',
                }),
            },
            fields: {
                client: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un cliente'
                        },
                    }
                },
                date_joined: {
                    validators: {
                        notEmpty: {
                            enabled: false,
                            message: 'La fecha es obligatoria'
                        },
                        date: {
                            format: 'YYYY-MM-DD',
                            message: 'La fecha no es válida'
                        }
                    }
                },
                type: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un tipo de venta'
                        },
                    }
                },
            },
        }
    )
        .on('core.element.validated', function (e) {
            if (e.valid) {
                const groupEle = FormValidation.utils.closest(e.element, '.form-group');
                if (groupEle) {
                    FormValidation.utils.classSet(groupEle, {
                        'has-success': false,
                    });
                }
                FormValidation.utils.classSet(e.element, {
                    'is-valid': false,
                });
            }
            const iconPlugin = fvSale.getPlugin('icon');
            const iconElement = iconPlugin && iconPlugin.icons.has(e.element) ? iconPlugin.icons.get(e.element) : null;
            iconElement && (iconElement.style.display = 'none');
        })
        .on('core.validator.validated', function (e) {
            if (!e.result.valid) {
                const messages = [].slice.call(fvSale.form.querySelectorAll('[data-field="' + e.field + '"][data-validator]'));
                messages.forEach((messageEle) => {
                    const validator = messageEle.getAttribute('data-validator');
                    messageEle.style.display = validator === e.validator ? 'block' : 'none';
                });
            }
        })
        .on('core.form.valid', function () {
            var parameters = new FormData(fvSale.form);
            ['input_search_products', 'cant', 'price'].forEach(function (value) {
                parameters.delete(value)
            });
            if (sale.details.products.length === 0) {
                message_error('Debe tener al menos un item en el detalle de la venta');
                return false;
            }
            parameters.append('products', JSON.stringify(sale.details.products));
            var list_url = fvSale.form.getAttribute('data-url');
            submit_formdata_with_ajax('Notificación',
                '¿Estas seguro de realizar la siguiente acción?',
                pathname,
                parameters,
                function (request) {
                    dialog_action('Notificación', '¿Desea Imprimir el Comprobante?', function () {
                        window.open(request.print_url, '_blank');
                        location.href = list_url;
                    }, function () {
                        location.href = list_url;
                    });
                },
            );
        });
});

$(function () {

    current_date = new moment().format("YYYY-MM-DD");
    input_search_products = $('input[name="search_products"]');
    select_client = $('select[name="client"]');
    input_birthdate = $('input[name="birthdate"]');
    input_date_joined = $('input[name="date_joined"]');

    /* Form */

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es",
    });

    input_date_joined.datetimepicker({
        useCurrent: false,
        format: 'YYYY-MM-DD',
        locale: 'es',
        keepOpen: false,
    });

    input_date_joined.on('change.datetimepicker', function (e) {
        fvSale.revalidateField('date_joined');
    });

    $('i[data-field="client"]').hide();
    $('i[data-field="input_search_products"]').hide();

    /* Product */

    input_search_products.autocomplete({
        source: function (request, response) {
            $.ajax({
                url: pathname,
                data: {
                    'action': 'search_products',
                    'term': request.term,
                    'ids': JSON.stringify(sale.getProductsIds()),
                },
                dataType: "json",
                type: "POST",
                headers: {
                    'X-CSRFToken': csrftoken
                },
                beforeSend: function () {

                },
                success: function (data) {
                    response(data);
                }
            });
        },
        min_length: 3,
        delay: 300,
        select: function (event, ui) {
            event.preventDefault();
            $(this).blur();
            if (ui.item.stock === 0 && ui.item.inventoried) {
                message_error('El stock de este producto esta en 0');
                return false;
            }
            ui.item.cant = 1;
            sale.addProduct(ui.item);
            $(this).val('').focus();
        }
    });

    $('.btnClearProducts').on('click', function () {
        input_search_products.val('').focus();
    });

    $('#tblProducts tbody')
        .off()
        .on('change', 'input[name="cant"]', function () {
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            sale.details.products[tr.row].cant = parseInt($(this).val());
            sale.calculateInvoice();
            $('td:last', tblProducts.row(tr.row).node()).html('$' + sale.details.products[tr.row].subtotal.toFixed(2));
        })
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            sale.details.products.splice(tr.row, 1);
            tblProducts.row(tr.row).remove().draw();
            sale.calculateInvoice();
        });

    $('.btnSearchProducts').on('click', function () {
        tblSearchProducts = $('#tblSearchProducts').DataTable({
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: {
                    'action': 'search_products',
                    'term': input_search_products.val(),
                    'ids': JSON.stringify(sale.getProductsIds()),
                },
                dataSrc: ""
            },
            columns: [
                {data: "code"},
                {data: "short_name"},
                {data: "price"},
                {data: "price_promotion"},
                {data: "stock"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-3, -4],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + data.toFixed(2);
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (row.stock > 0) {
                            return '<span class="badge badge-success badge-pill">' + row.stock + '</span>';
                        }
                        return '<span class="badge badge-danger badge-pill">' + row.stock + '</span>';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<a rel="add" class="btn btn-success btn-flat btn-xs"><i class="fas fa-plus"></i></a>';
                    }
                }
            ],
            rowCallback: function (row, data, index) {

            },
            initComplete: function (settings, json) {
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
        $('#myModalSearchProducts').modal('show');
    });

    $('#tblSearchProducts tbody')
        .off()
        .on('click', 'a[rel="add"]', function () {
            var row = tblSearchProducts.row($(this).parents('tr')).data();
            row.cant = 1;
            sale.addProduct(row);
            tblSearchProducts.row($(this).parents('tr')).remove().draw();
        });

    $('.btnRemoveAllProducts').on('click', function () {
        if (sale.details.products.length === 0) return false;
        dialog_action('Notificación', '¿Estas seguro de eliminar todos los items de tu detalle?', function () {
            sale.details.products = [];
            sale.listProducts();
        });
    });

    /* Client */

    select_client.select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        // dropdownParent: modal_sale,
        ajax: {
            delay: 250,
            type: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            url: pathname,
            data: function (params) {
                return {
                    term: params.term,
                    action: 'search_client'
                };
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese una descripción',
        minimumInputLength: 1,
    })
        .on('select2:select', function (e) {
            fvSale.revalidateField('client');
        })
        .on('select2:clear', function (e) {
            fvSale.revalidateField('client');
        });

    $('.btnAddClient').on('click', function () {
        input_birthdate.datetimepicker('date', new Date());
        $('#myModalClient').modal('show');
    });

    $('#myModalClient').on('hidden.bs.modal', function () {
        fvClient.resetForm(true);
    });

    $('input[name="dni"]').on('keypress', function (e) {
        return validate_form_text('numbers', e, null);
    });

    $('input[name="mobile"]').on('keypress', function (e) {
        return validate_form_text('numbers', e, null);
    });

    input_birthdate.datetimepicker({
        useCurrent: false,
        format: 'YYYY-MM-DD',
        locale: 'es',
        keepOpen: false,
        // maxDate: current_date
    });

    input_birthdate.on('change.datetimepicker', function (e) {
        fvClient.revalidateField('birthdate');
    });
});