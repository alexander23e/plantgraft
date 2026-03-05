var fv;
var input_search_resources, input_search_products, input_date_joined;
var tblResources, tblSearchResources, tblSearchProducts, tblProducts;

var production = {
    details: {
        resources: [],
        products: []
    },
    // resources
    listResources: function () {
        tblResources = $('#tblResources').DataTable({
            autoWidth: false,
            destroy: true,
            data: this.details.resources,
            ordering: false,
            lengthChange: false,
            searching: false,
            paginate: false,
            columns: [
                {data: "id"},
                {data: "code"},
                {data: "short_name"},
                {data: "stock"},
                {data: "cant"},
            ],
            columnDefs: [
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return data;
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<input type="text" class="form-control" autocomplete="off" name="cant" value="' + row.cant + '">';
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
                        max: data.stock,
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
    getResourcesIds: function () {
        return this.details.resources.map(value => value.id);
    },
    addResource: function (item) {
        this.details.resources.push(item);
        this.listResources();
    },
    // products
    listProducts: function () {
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
                {data: "name"},
                {data: "type.name"},
                {data: "cant"},
            ],
            columnDefs: [
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        var name = row.type.name;
                        if (row.type.id === 'plant') {
                            return '<span class="badge badge-primary badge-pill">' + name + '</span>';
                        }
                        return '<span class="badge badge-info badge-pill">' + name + '</span>';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<input type="text" class="form-control" autocomplete="off" name="cant" value="' + row.cant + '">';
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
                        max: 10000000,
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
    fv = FormValidation.formValidation(document.getElementById('frmForm'), {
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
                lot: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un lote'
                        },
                    }
                },
                product: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un producto de cacao'
                        },
                    }
                },
                date_joined: {
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
            const iconPlugin = fv.getPlugin('icon');
            const iconElement = iconPlugin && iconPlugin.icons.has(e.element) ? iconPlugin.icons.get(e.element) : null;
            iconElement && (iconElement.style.display = 'none');
        })
        .on('core.validator.validated', function (e) {
            if (!e.result.valid) {
                const messages = [].slice.call(fv.form.querySelectorAll('[data-field="' + e.field + '"][data-validator]'));
                messages.forEach((messageEle) => {
                    const validator = messageEle.getAttribute('data-validator');
                    messageEle.style.display = validator === e.validator ? 'block' : 'none';
                });
            }
        })
        .on('core.form.valid', function () {
            var parameters = new FormData(fv.form);
            if (production.details.products.length === 0) {
                message_error('Debe agregar al menos un producto al detalle de la producción');
            }
            parameters.append('products', JSON.stringify(production.details.products));
            parameters.append('resources', JSON.stringify(production.details.resources));
            submit_formdata_with_ajax('Alerta', '¿Estas seguro de realizar la siguiente acción?', pathname, parameters, function () {
                location.href = fv.form.getAttribute('data-url');
            });
        });
});

$(function () {
    input_date_joined = $('input[name="date_joined"]');
    input_search_resources = $('input[name="search_resources"]');
    input_search_products = $('input[name="search_products"]');

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es"
    });

    $('select[name="lot"]').on('change', function () {
        fv.revalidateField('lot');
    });

    $('select[name="product"]').on('change', function () {
        fv.revalidateField('product');
    });

    input_date_joined.datetimepicker({
        useCurrent: false,
        format: 'YYYY-MM-DD',
        locale: 'es',
        keepOpen: false,
    });

    input_date_joined.on('change.datetimepicker', function (e) {
        fv.revalidateField('date_joined');
    });

    /* Resources */

    input_search_resources.autocomplete({
        source: function (request, response) {
            $.ajax({
                url: pathname,
                data: {
                    'action': 'search_resources',
                    'term': request.term,
                    'ids': JSON.stringify(production.getResourcesIds()),
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
            ui.item.cant = 1;
            production.addResource(ui.item);
            $(this).val('').focus();
        }
    });

    $('.btnClearResources').on('click', function () {
        input_search_resources.val('').focus();
    });

    $('#tblResources tbody')
        .off()
        .on('change', 'input[name="cant"]', function () {
            var tr = tblResources.cell($(this).closest('td, li')).index();
            production.details.resources[tr.row].cant = parseInt($(this).val());
        })
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblResources.cell($(this).closest('td, li')).index();
            production.details.resources.splice(tr.row, 1);
            tblResources.row(tr.row).remove().draw();
            $('.tooltip').remove();
        });

    $('.btnSearchResources').on('click', function () {
        tblSearchResources = $('#tblSearchResources').DataTable({
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: {
                    'action': 'search_resources',
                    'term': input_search_resources.val(),
                    'ids': JSON.stringify(production.getResourcesIds()),
                },
                dataSrc: ""
            },
            columns: [
                {data: "code"},
                {data: "short_name"},
                {data: "category.name"},
                {data: "price"},
                {data: "stock"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-3],
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
                            return '<span class="badge badge-success badge-pill">' + data + '</span>'
                        }
                        return '<span class="badge badge-warning badge-pill">' + data + '</span>'
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<a rel="add" class="btn btn-success btn-flat btn-xs"><i class="fas fa-plus"></i></a>'
                    }
                }
            ],
            rowCallback: function (row, data, index) {
                var tr = $(row).closest('tr');
                if (data.stock === 0) {
                    $(tr).css({'background': '#dc3345', 'color': 'white'});
                }
            },
            initComplete: function (settings, json) {
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
        $('#myModalSearchResources').modal('show');
    });

    $('#myModalSearchResources').on('shown.bs.modal', function () {
        production.listResources();
    });

    $('#tblSearchResources tbody')
        .off()
        .on('click', 'a[rel="add"]', function () {
            var row = tblSearchResources.row($(this).parents('tr')).data();
            row.cant = 1;
            production.addResource(row);
            tblSearchResources.row($(this).parents('tr')).remove().draw();
        });

    $('.btnRemoveAllResources').on('click', function () {
        if (production.details.resources.length === 0) return false;
        dialog_action('Notificación', '¿Estas seguro de eliminar todos los items de tu detalle?', function () {
            production.details.resources = [];
            production.listResources();
        }, function () {

        });
    });

    /* Products */

    input_search_products.autocomplete({
        source: function (request, response) {
            $.ajax({
                url: pathname,
                data: {
                    'action': 'search_products',
                    'term': request.term,
                    'ids': JSON.stringify(production.getProductsIds()),
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
            ui.item.cant = 1;
            production.addProduct(ui.item);
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
            production.details.products[tr.row].cant = parseInt($(this).val());
        })
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            production.details.products.splice(tr.row, 1);
            tblProducts.row(tr.row).remove().draw();
            $('.tooltip').remove();
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
                    'ids': JSON.stringify(production.getProductsIds()),
                },
                dataSrc: ""
            },
            columns: [
                {data: "id"},
                {data: "name"},
                {data: "type.name"},
                {data: "stock"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return data;
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (row.stock > 0) {
                            return '<span class="badge badge-success badge-pill">' + data + '</span>'
                        }
                        return '<span class="badge badge-warning badge-pill">' + data + '</span>'
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<a rel="add" class="btn btn-success btn-flat btn-xs"><i class="fas fa-plus"></i></a>'
                    }
                }
            ],
            rowCallback: function (row, data, index) {
                var tr = $(row).closest('tr');
                if (data.stock === 0) {
                    $(tr).css({'background': '#dc3345', 'color': 'white'});
                }
            },
            initComplete: function (settings, json) {
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
        $('#myModalSearchProducts').modal('show');
    });

    $('#myModalSearchProducts').on('shown.bs.modal', function () {
        production.listProducts();
    });

    $('#tblSearchProducts tbody')
        .off()
        .on('click', 'a[rel="add"]', function () {
            var row = tblSearchProducts.row($(this).parents('tr')).data();
            row.cant = 1;
            production.addProduct(row);
            tblSearchProducts.row($(this).parents('tr')).remove().draw();
        });

    $('.btnRemoveAllProducts').on('click', function () {
        if (production.details.products.length === 0) return false;
        dialog_action('Notificación', '¿Estas seguro de eliminar todos los items de tu detalle?', function () {
            production.details.products = [];
            production.listProducts();
        }, function () {

        });
    });
});