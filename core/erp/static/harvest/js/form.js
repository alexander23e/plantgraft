var select_production;
var input_date_joined;
var fv;
var tblProducts = null;

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
                production: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione una producción'
                        }
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
            var products = harvest.getProducts();
            if ($.isEmptyObject(products)) {
                message_error('Debe al menos tener un item en el detalle activo');
                return false;
            }
            parameters.append('products', JSON.stringify(products));
            submit_formdata_with_ajax('Alerta', '¿Estas seguro de realizar la siguiente acción?', pathname, parameters, function () {
                alert_sweetalert('success', 'Alerta', 'Datos registrados correctamente', function () {
                    location.reload();
                }, 2500, null);
            });
        });
});

var harvest = {
    searchProduction: function () {
        var id = select_production.val();
        if ($.isEmptyObject(id)) {
            if (tblProducts) tblProducts.clear().draw();
            return false;
        }
        tblProducts = $('#tblProducts').DataTable({
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: {
                    'action': 'search_production',
                    'id': id
                },
                dataSrc: "products"
            },
            ordering: false,
            lengthChange: false,
            searching: false,
            paginate: false,
            columns: [
                {data: "id"},
                {data: "product.name"},
                {data: "product.type.name"},
                {data: "cant"},
                {data: "current_stage.name"},
                {data: "status.name"},
                {data: "harvest_date"},
                {data: "loss"},
                {data: "total"},
            ],
            columnDefs: [
                {
                    targets: [-7],
                    class: 'text-center',
                    render: function (data, type, row) {
                        var name = row.product.type.name;
                        if (row.product.type.id === 'plant') {
                            return '<span class="badge badge-primary badge-pill">' + name + '</span>';
                        }
                        return '<span class="badge badge-info badge-pill">' + name + '</span>';
                    }
                },
                {
                    targets: [-5],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<a rel="stages" style="background-color: ' + row.current_stage.color + '" class="badge badge-secondary badge-pill cursor-pointer">' + data + '</a>';
                    }
                },
                {
                    targets: [-4],
                    class: 'text-center',
                    render: function (data, type, row) {
                        var name = row.status.name;
                        switch (row.status.id) {
                            case "in_process":
                                return '<span class="badge badge-primary badge-pill">' + name + '</span>';
                            case "finished":
                                return '<span class="badge badge-info badge-pill">' + name + '</span>';
                            case "harvested":
                                return '<span class="badge badge-success badge-pill">' + name + '</span>';
                        }
                    }
                },
                {
                    targets: [-3, -6],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return data;
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (row.status.id === 'finished') {
                            return '<input type="text" disabled name="loss" class="form-control" value="' + row.loss + '">';
                        }
                        return row.loss;
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return data;
                    }
                },
                {
                    targets: [0],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (row.status.id === 'finished') {
                            return '<div class="form-group form-check mb-0"><input type="checkbox" class="form-control-checkbox" name="state"></div>';
                        }
                        return '--';
                    }
                },
            ],
            rowCallback: function (row, data, index) {
                var tr = $(row).closest('tr');
                tr.find('input[name="loss"]')
                    .TouchSpin({
                        min: 0,
                        max: data.cant
                    })
                    .on('keypress', function (e) {
                        return validate_form_text('numbers', e, null);
                    });
            },
            initComplete: function (settings, json) {
                if (!json.production.state) {
                    alert_sweetalert('info', 'Alerta', 'La producción ' + json.production.number + ' ya ha finalizado', function () {
                        $('.btn').hide();
                    }, 1500, null);
                } else {
                    $('.btn').show();
                }
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
    },
    getProducts: function () {
        if (tblProducts) {
            return tblProducts.rows().data().toArray().filter(value => value.status.id === 'finished' && value.state === 1);
        }
        return [];
    }
};

$(function () {
    input_date_joined = $('input[name="date_joined"]');
    select_production = $('select[name="production"]');

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es"
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

    select_production.on('change', function () {
        fv.revalidateField('production');
        harvest.searchProduction();
    });

    $('#tblProducts tbody')
        .off()
        .on('change', 'input[name="state"]', function () {
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            var row = tblProducts.row(tr.row).data();
            row.state = this.checked ? 1 : 0;
            $('td', tblProducts.row(tr.row).node()).find('input[name="loss"]').prop('disabled', !this.checked);
        })
        .on('change', 'input[name="loss"]', function () {
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            var row = tblProducts.row(tr.row).data();
            row.loss = parseInt($(this).val());
            row.total = row.cant - row.loss;
            $('td:last', tblProducts.row(tr.row).node()).html(row.total);
        })
        .on('click', 'a[rel="stages"]', function () {
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            var row = tblProducts.row(tr.row).data();
            $('#tblStages').DataTable({
                autoWidth: false,
                destroy: true,
                paging: false,
                info: false,
                ajax: {
                    url: pathname,
                    type: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                    data: {
                        'action': 'search_detail_stages',
                        'id': row.id
                    },
                    dataSrc: ""
                },
                columns: [
                    {data: "date_joined"},
                    {data: "stage.name"},
                    {data: "observations"},
                ],
                columnDefs: [
                    {
                        targets: [-2],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return '<span class="badge badge-secondary badge-pill" style="background-color: ' + row.stage.color + '">' + data + '</span>';
                        }
                    },
                ],
                initComplete: function (settings, json) {
                    $(this).wrap('<div class="dataTables_scroll"><div/>');
                }
            });
            $('#myModalStages').modal('show');
        });

    $('#select_all').on('change', function () {
        var state = this.checked;
        if (tblProducts) {
            var cells = tblProducts.cells().nodes();
            $(cells).find('input[name="state"]').prop('checked', state).trigger('change');
        }
    });

    $('.btn').hide();
});