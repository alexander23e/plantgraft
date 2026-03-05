var tblResources, tblSearchResources;
var current_date;
var fvPurchase, fvProvider;
var select_provider;
var input_date_joined, input_search_resources;

var purchase = {
    details: {
        resources: [],
    },
    calculateInvoice: function () {
        var subtotal = 0.00;
        this.details.resources.forEach(function (value, index, array) {
            value.subtotal = value.cant * value.price;
            subtotal += value.subtotal;
        });
        $('.subtotal').html('$' + subtotal.toFixed(2));
    },
    listResources: function () {
        this.calculateInvoice();
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
                {data: "cant"},
                {data: "price"},
                {data: "subtotal"},
            ],
            columnDefs: [
                {
                    targets: [-3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<input type="text" class="form-control" autocomplete="off" name="cant" value="' + row.cant + '">';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + data.toFixed(2);
                    }
                },
                {
                    targets: [-2],
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
    getResourcesIds: function () {
        return this.details.resources.map(value => value.id);
    },
    addResource: function (item) {
        this.details.resources.push(item);
        this.listResources();
    },
};

document.addEventListener('DOMContentLoaded', function (e) {
    fvPurchase = FormValidation.formValidation(document.getElementById('frmPurchase'), {
            locale: 'es_ES',
            localization: FormValidation.locales.es_ES,
            plugins: {
                trigger: new FormValidation.plugins.Trigger(),
                submitButton: new FormValidation.plugins.SubmitButton(),
                bootstrap: new FormValidation.plugins.Bootstrap(),
                excluded: new FormValidation.plugins.Excluded(),
                icon: new FormValidation.plugins.Icon({
                    valid: 'fa fa-check',
                    invalid: 'fa fa-times',
                    validating: 'fa fa-refresh',
                }),
            },
            fields: {
                number: {
                    validators: {
                        notEmpty: {},
                        digits: {},
                        stringLength: {
                            min: 8,
                        },
                        remote: {
                            url: pathname,
                            data: function () {
                                return {
                                    pattern: 'number',
                                    number: fvPurchase.form.querySelector('[name="number"]').value,
                                    action: 'validate_purchase'
                                };
                            },
                            message: 'El número de factura ya se encuentra registrado',
                            method: 'POST',
                            headers: {
                                'X-CSRFToken': csrftoken
                            },
                        }
                    }
                },
                payment_condition: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione una forma de pago'
                        },
                    }
                },
                provider: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un proveedor'
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
                    }
                },
                end_credit: {
                    validators: {
                        notEmpty: {
                            message: 'La fecha es obligatoria'
                        },
                        date: {
                            format: 'YYYY-MM-DD',
                            message: 'La fecha no es válida'
                        }
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
            const iconPlugin = fvPurchase.getPlugin('icon');
            const iconElement = iconPlugin && iconPlugin.icons.has(e.element) ? iconPlugin.icons.get(e.element) : null;
            iconElement && (iconElement.style.display = 'none');
        })
        .on('core.validator.validated', function (e) {
            if (!e.result.valid) {
                const messages = [].slice.call(fvPurchase.form.querySelectorAll('[data-field="' + e.field + '"][data-validator]'));
                messages.forEach((messageEle) => {
                    const validator = messageEle.getAttribute('data-validator');
                    messageEle.style.display = validator === e.validator ? 'block' : 'none';
                });
            }
        })
        .on('core.form.valid', function () {
            var parameters = new FormData(fvPurchase.form);
            if (purchase.details.resources.length === 0) {
                message_error('Debe tener al menos un item en el detalle');
                return false;
            }
            parameters.append('resources', JSON.stringify(purchase.details.resources));
            submit_formdata_with_ajax('Notificación',
                '¿Estas seguro de realizar la siguiente acción?',
                pathname,
                parameters,
                function () {
                    location.href = fvPurchase.form.getAttribute('data-url');
                },
            );
        });
});

document.addEventListener('DOMContentLoaded', function (e) {
    fvProvider = FormValidation.formValidation(document.getElementById('frmProvider'), {
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
                name: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
                        },
                        remote: {
                            url: pathname,
                            data: function () {
                                return {
                                    parameter: fvProvider.form.querySelector('[name="name"]').value,
                                    pattern: 'name',
                                    action: 'validate_provider'
                                };
                            },
                            message: 'El nombre ya se encuentra registrado',
                            method: 'POST',
                            headers: {
                                'X-CSRFToken': csrftoken
                            },
                        }
                    }
                },
                ruc: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 13
                        },
                        digits: {},
                        remote: {
                            url: pathname,
                            data: function () {
                                return {
                                    parameter: fvProvider.form.querySelector('[name="ruc"]').value,
                                    pattern: 'ruc',
                                    action: 'validate_provider'
                                };
                            },
                            message: 'El número de ruc ya se encuentra registrado',
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
                            min: 10
                        },
                        digits: {},
                        remote: {
                            url: pathname,
                            data: function () {
                                return {
                                    parameter: fvProvider.form.querySelector('[name="mobile"]').value,
                                    pattern: 'mobile',
                                    action: 'validate_provider'
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
                        notEmpty: {},
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
                                    parameter: fvProvider.form.querySelector('[name="email"]').value,
                                    pattern: 'email',
                                    action: 'validate_provider'
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
                        // stringLength: {
                        //     min: 4,
                        // }
                    }
                }
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
            const iconPlugin = fvProvider.getPlugin('icon');
            const iconElement = iconPlugin && iconPlugin.icons.has(e.element) ? iconPlugin.icons.get(e.element) : null;
            iconElement && (iconElement.style.display = 'none');
        })
        .on('core.validator.validated', function (e) {
            if (!e.result.valid) {
                const messages = [].slice.call(fvProvider.form.querySelectorAll('[data-field="' + e.field + '"][data-validator]'));
                messages.forEach((messageEle) => {
                    const validator = messageEle.getAttribute('data-validator');
                    messageEle.style.display = validator === e.validator ? 'block' : 'none';
                });
            }
        })
        .on('core.form.valid', function () {
            var parameters = new FormData(fvProvider.form);
            parameters.append('action', 'create_provider');
            submit_formdata_with_ajax('Notificación', '¿Estas seguro de realizar la siguiente acción?', pathname,
                parameters,
                function (request) {
                    var newOption = new Option(request.name + ' / ' + request.ruc, request.id, false, true);
                    select_provider.append(newOption).trigger('change');
                    fvPurchase.revalidateField('provider');
                    $('#myModalProvider').modal('hide');
                }
            );
        });
});

$(function () {

    current_date = new moment().format("YYYY-MM-DD");
    input_date_joined = $('input[name="date_joined"]');
    select_provider = $('select[name="provider"]');
    input_search_resources = $('input[name="search_resources"]');

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es",
    });

    /* Resources */

    input_search_resources.autocomplete({
        source: function (request, response) {
            $.ajax({
                url: pathname,
                data: {
                    'action': 'search_resources',
                    'term': request.term,
                    'ids': JSON.stringify(purchase.getResourcesIds()),
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
            purchase.addResource(ui.item);
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
            purchase.details.resources[tr.row].cant = parseInt($(this).val());
            purchase.calculateInvoice();
            $('td:last', tblResources.row(tr.row).node()).html('$' + purchase.details.resources[tr.row].subtotal.toFixed(2));
        })
        .on('change', 'input[name="price"]', function () {
            var tr = tblResources.cell($(this).closest('td, li')).index();
            purchase.details.resources[tr.row].price = parseFloat($(this).val());
            purchase.calculateInvoice();
            $('td:last', tblResources.row(tr.row).node()).html('$' + purchase.details.resources[tr.row].subtotal.toFixed(2));
        })
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblResources.cell($(this).closest('td, li')).index();
            purchase.details.resources.splice(tr.row, 1);
            tblResources.row(tr.row).remove().draw();
            purchase.calculateInvoice();
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
                    'ids': JSON.stringify(purchase.getResourcesIds()),
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
            order: [[4, 'desc']],
            rowCallback: function (row, data, index) {
                if (data.stock === 0) {
                    $(row).addClass('low-stock');
                }
            },
            initComplete: function (settings, json) {
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
        $('#myModalSearchResources').modal('show');
    });

    $('#myModalSearchResources').on('shown.bs.modal', function () {
        purchase.listResources();
    });

    $('#tblSearchResources tbody')
        .off()
        .on('click', 'a[rel="add"]', function () {
            var row = tblSearchResources.row($(this).parents('tr')).data();
            row.cant = 1;
            purchase.addResource(row);
            tblSearchResources.row($(this).parents('tr')).remove().draw();
        });

    $('.btnRemoveAllResources').on('click', function () {
        if (purchase.details.resources.length === 0) return false;
        dialog_action('Notificación', '¿Estas seguro de eliminar todos los items de tu detalle?', function () {
            purchase.details.resources = [];
            purchase.listResources();
        }, function () {

        });
    });

    /* Search Provider */

    select_provider.select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
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
                    action: 'search_provider'
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
            fvPurchase.revalidateField('provider');
        })
        .on('select2:clear', function (e) {
            fvPurchase.revalidateField('provider');
        });

    $('.btnAddProvider').on('click', function () {
        $('#myModalProvider').modal('show');
    });

    $('#myModalProvider').on('hidden.bs.modal', function () {
        fvProvider.resetForm(true);
    });

    $('input[name="ruc"]').on('keypress', function (e) {
        return validate_form_text('numbers', e, null);
    });

    $('input[name="mobile"]').on('keypress', function (e) {
        return validate_form_text('numbers', e, null);
    });

    /* Form */

    $('input[name="number"]').on('keypress', function (e) {
        return validate_form_text('numbers', e, null);
    });

    input_date_joined.datetimepicker({
        format: 'YYYY-MM-DD',
        useCurrent: false,
        locale: 'es',
        orientation: 'bottom',
        keepOpen: false
    });

    input_date_joined.on('change.datetimepicker', function (e) {
        fvPurchase.revalidateField('date_joined');
    });

    $('i[data-field="provider"]').hide();
    $('i[data-field="input_search_resources"]').hide();
});