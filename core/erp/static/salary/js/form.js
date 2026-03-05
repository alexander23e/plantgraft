var tblSalary = null, tblIngress, tblEgress;
var fv;
var input_year_month;
var salary = {
    calculate: function () {
        var rows = tblSalary.rows().data().toArray();
        rows.forEach(function (value, index, array) {
            value.ingress_total = value.ingress.reduce((a, b) => a + (parseFloat(b.total) || 0), 0);
            value.egress_total = value.egress.reduce((a, b) => a + (parseFloat(b.total) || 0), 0);
            value.total = parseFloat(value.rmu_month) - parseFloat(value.ingress_total) + parseFloat(value.egress_total) - parseFloat(value.loan_discount);
        });
        this.list(rows);
    },
    generate: function () {
        var parameters = {
            'year': input_year_month.datetimepicker('date').format("YYYY"),
            'month': input_year_month.datetimepicker('date').format("MM"),
            'action': 'generate_salary'
        };

        $.ajax({
            url: pathname,
            data: parameters,
            type: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            dataType: 'json',
            success: function (request) {
                if (!request.hasOwnProperty('error')) {
                    salary.list(request);
                    return false;
                }
                message_error(request.error);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                message_error(errorThrown + ' ' + textStatus);
            }
        });
    },
    list: function (items) {
        tblSalary = $('#tblSalary').DataTable({
            autoWidth: false,
            destroy: true,
            data: items,
            columns: [
                {"data": "employee.names"},
                {"data": "rmu"},
                {"data": "salary_by_day"},
                {"data": "days_work"},
                {"data": "rmu_month"},
                {"data": "ingress_total"},
                {"data": "egress_total"},
                {"data": "loan_discount"},
                {"data": "total"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [-2, -3, -4, -5, -6, -8, -9],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + data.toFixed(2);
                    }
                },
                {
                    targets: [0],
                    class: 'text-left',
                    render: function (data, type, row) {
                        return row.names + " (" + row.dni + ")";
                    }
                },
                {
                    targets: [-7],
                    class: 'text-center',
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<a rel="detail" class="btn bg-navy btn-flat btn-xs"><i class="fas fa-dollar-sign"></i></a>';
                    }
                },
            ],
            initComplete: function (settings, json) {
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
    }
};

document.addEventListener('DOMContentLoaded', function (e) {
    fv = FormValidation.formValidation(document.getElementById('frmForm'), {
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
                year_month: {
                    validators: {
                        notEmpty: {},
                        regexp: {
                            regexp: /^([0-9]{1,2}([/][0-9]{2}))+$/i,
                            message: 'Debe ingresar el mes y el año en el siguiente formato 01/20'
                        },
                        remote: {
                            url: pathname,
                            data: function () {
                                return {
                                    year: input_year_month.datetimepicker('date').format("YYYY"),
                                    month: input_year_month.datetimepicker('date').format("MM"),
                                    action: 'validate_data'
                                };
                            },
                            message: 'El rol de pago ya esta registrado',
                            method: 'POST',
                            headers: {
                                'X-CSRFToken': csrftoken
                            },
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
            parameters.append('year', input_year_month.datetimepicker('date').format("YYYY"));
            parameters.append('month', input_year_month.datetimepicker('date').format("MM"));
            parameters.append('salaries', JSON.stringify(tblSalary.rows().data().toArray()));
            submit_formdata_with_ajax('Notificación',
                '¿Estas seguro de realizar la siguiente acción?',
                pathname,
                parameters,
                function (request) {
                    location.href = fv.form.getAttribute('data-url');
                },
            );
        });
});

$(function () {
    input_year_month = $('input[name="year_month"]');

    input_year_month.datetimepicker({
        viewMode: 'years',
        format: 'MM/YY',
        useCurrent: false,
        locale: 'es',
        date: new Date(),
    });

    input_year_month.on('hide.datetimepicker change.datetimepicker', function (e) {
        fv.validateField('year_month').then(function (status) {
            if (status === 'Valid') {
                salary.generate();
            } else if (tblSalary !== null) {
                tblSalary.clear().draw();
            }
        });
    });

    $('#tblSalary tbody')
        .off()
        .on('click', 'a[rel="detail"]', function () {
            $('.tooltip').remove();
            var td = tblSalary.cell($(this).closest('td, li')).index(),
                row = tblSalary.row(td.row).data();
            $('input[name="net_salary"]').val(row.rmu_month);
            tblIngress = $('#tblIngress').DataTable({
                autoWidth: false,
                destroy: true,
                paging: false,
                data: row.ingress,
                columns: [
                    {"data": "name"},
                    {"data": "valor"},
                    {"data": "cant"},
                    {"data": "total"},
                ],
                columnDefs: [
                    {
                        targets: [-3],
                        class: 'text-center',
                        render: function (data, type, row) {
                            if (['salary', 'value'].includes(row.calculation_method.id)) {
                                return row.valor;
                            }
                            return '---';
                        }
                    },
                    {
                        targets: [-2],
                        class: 'text-center',
                        render: function (data, type, row) {
                            if (row.calculation_method.id === 'salary') {
                                return row.cant;
                            }
                            return '<input type="text" class="form-control form-control-sm" name="cant" autocomplete="off" value="' + row.cant + '">';
                        }
                    },
                    {
                        targets: [-1],
                        class: 'text-center',
                        render: function (data, type, row) {
                            if (['salary', 'value'].includes(row.calculation_method.id)) {
                                return parseFloat(row.total).toFixed(2);
                            }
                            return '<input type="text" class="form-control form-control-sm" name="total" autocomplete="off" value="' + row.total + '">';
                        }
                    },
                ],
                rowCallback: function (row, data, index) {
                    var tr = $(row).closest('tr');
                    tr.find('input[name="cant"]')
                        .TouchSpin({
                            min: 0.00,
                            max: 1000000,
                            step: 0.01,
                            decimals: 2,
                            boostat: 5,
                            maxboostedstep: 10,
                            buttondown_class: 'btn btn-secondary btn-sm',
                            buttonup_class: 'btn btn-secondary btn-sm',
                        })
                        .on('keypress', function (e) {
                            return validate_form_text('numbers', e, null);
                        });
                    tr.find('input[name="total"]')
                        .TouchSpin({
                            min: 0.00,
                            max: 1000000,
                            step: 0.01,
                            decimals: 2,
                            boostat: 5,
                            maxboostedstep: 10,
                            buttondown_class: 'btn btn-secondary btn-sm',
                            buttonup_class: 'btn btn-secondary btn-sm',
                        })
                        .on('keypress', function (e) {
                            return validate_form_text('numbers', e, null);
                        });
                },
                initComplete: function (settings, json) {
                    $(this).wrap('<div class="dataTables_scroll"><div/>');
                }
            });
            tblEgress = $('#tblEgress').DataTable({
                autoWidth: false,
                destroy: true,
                paging: false,
                data: row.egress,
                columns: [
                    {"data": "name"},
                    {"data": "valor"},
                    {"data": "cant"},
                    {"data": "total"},
                ],
                columnDefs: [
                    {
                        targets: [-3],
                        class: 'text-center',
                        render: function (data, type, row) {
                            if (['salary', 'value'].includes(row.calculation_method.id)) {
                                return row.valor;
                            }
                            return '---';
                        }
                    },
                    {
                        targets: [-2],
                        class: 'text-center',
                        render: function (data, type, row) {
                            if (row.calculation_method.id === 'salary') {
                                return row.cant;
                            }
                            return '<input type="text" class="form-control form-control-sm" name="cant" autocomplete="off" value="' + row.cant + '">';
                        }
                    },
                    {
                        targets: [-1],
                        class: 'text-center',
                        render: function (data, type, row) {
                            if (['salary', 'value'].includes(row.calculation_method.id)) {
                                return parseFloat(row.total).toFixed(2);
                            }
                            return '<input type="text" class="form-control form-control-sm" name="total" autocomplete="off" value="' + row.total + '">';
                        }
                    },
                ],
                rowCallback: function (row, data, index) {
                    var tr = $(row).closest('tr');
                    tr.find('input[name="cant"]')
                        .TouchSpin({
                            min: 0.00,
                            max: 1000000,
                            step: 0.01,
                            decimals: 2,
                            boostat: 5,
                            maxboostedstep: 10,
                            buttondown_class: 'btn btn-secondary btn-sm',
                            buttonup_class: 'btn btn-secondary btn-sm',
                        })
                        .on('keypress', function (e) {
                            return validate_form_text('numbers', e, null);
                        });
                    tr.find('input[name="total"]')
                        .TouchSpin({
                            min: 0.00,
                            max: 1000000,
                            step: 0.01,
                            decimals: 2,
                            boostat: 5,
                            maxboostedstep: 10,
                            buttondown_class: 'btn btn-secondary btn-sm',
                            buttonup_class: 'btn btn-secondary btn-sm',
                        })
                        .on('keypress', function (e) {
                            return validate_form_text('numbers', e, null);
                        });
                },
                initComplete: function (settings, json) {
                    $(this).wrap('<div class="dataTables_scroll"><div/>');
                }
            });
            $('#tblAssistance').DataTable({
                autoWidth: false,
                destroy: true,
                ajax: {
                    url: pathname,
                    type: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                    data: {
                        'action': 'search_assistance',
                        'employee': row.id,
                        'year': input_year_month.datetimepicker('date').format("YYYY"),
                        'month': input_year_month.datetimepicker('date').format("MM"),
                    },
                    dataSrc: ""
                },
                columns: [
                    {"data": "date_joined"},
                    {"data": "state"},
                    {"data": "details"},
                ],
                columnDefs: [
                    {
                        targets: [-2],
                        class: 'text-center',
                        render: function (data, type, row) {
                            if (row.state) {
                                return '<span class="badge badge-success badge-pill">Si</span>';
                            }
                            return '<span class="badge badge-danger badge-pill">No</span>';
                        }
                    },
                ],
                initComplete: function (settings, json) {
                    $(this).wrap('<div class="dataTables_scroll"><div/>');
                }
            });
            $('.nav-tabs a[href="#home"]').tab('show');
            $('#myModalHeadings').modal('show');
        });

    $('#tblIngress tbody')
        .off()
        .on('change', 'input[name="cant"]', function () {
            var tr = tblIngress.cell($(this).closest('td, li')).index();
            var data = tblIngress.row(tr.row).data();
            data.cant = parseFloat($(this).val());
            if (data.calculation_method.id === 'value') {
                data.total = data.cant * data.valor;
                $('td:last', tblIngress.row(tr.row).node()).html(data.total.toFixed(2));
            }
        })
        .on('change', 'input[name="total"]', function () {
            var tr = tblIngress.cell($(this).closest('td, li')).index();
            var data = tblIngress.row(tr.row).data();
            data.total = parseFloat($(this).val());
        });

    $('#tblEgress tbody')
        .off()
        .on('change', 'input[name="cant"]', function () {
            var tr = tblEgress.cell($(this).closest('td, li')).index();
            var data = tblEgress.row(tr.row).data();
            data.cant = parseFloat($(this).val());
            if (data.calculation_method.id === 'value') {
                data.total = data.cant * data.valor;
                $('td:last', tblEgress.row(tr.row).node()).html(data.total.toFixed(2));
            }
        })
        .on('change', 'input[name="total"]', function () {
            var tr = tblEgress.cell($(this).closest('td, li')).index();
            var data = tblEgress.row(tr.row).data();
            data.total = parseFloat($(this).val());
        });

    input_year_month.trigger('change');

    $('#myModalHeadings').on('hidden.bs.modal', function (e) {
        salary.calculate();
    });

    if ($('input[name="action"]').val() === 'edit') {
        salary.generate();
    }
});