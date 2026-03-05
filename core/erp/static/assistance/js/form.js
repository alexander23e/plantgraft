var tblAssistance = null;
var input_date_joined;
var fv;

var assistance = {
    listAssistances: function () {
        tblAssistance = $('#tblAssistance').DataTable({
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: {
                    'action': 'generate_assistance',
                    'date_joined': input_date_joined.val()
                },
                dataSrc: ""
            },
            ordering: false,
            lengthChange: false,
            paging: false,
            columns: [
                {data: "names"},
                {data: "dni"},
                {data: "mobile"},
                {data: "email"},
                {data: "details"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<input type="text" name="details" class="form-control form-control-sm" placeholder="Ingrese una observación" value="' + data + '" autocomplete="off">';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        var attr = row.state === 1 ? ' checked' : '';
                        return '<input type="checkbox" name="state" class="form-control-checkbox" ' + attr + '>';
                    }
                },
            ],
            rowCallback: function (row, data, index) {
                var tr = $(row).closest('tr');
                var background = data.state === 0 ? '#fff' : '#fff0d7';
                $(tr).css('background', background);
                tr.find('input[type="text"]').prop('disabled', data.state === 1);
            },
            initComplete: function (settings, json) {
                $('[data-toggle="tooltip"]').tooltip();
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
    },
    getAssistances: function () {
        return tblAssistance.rows().data().toArray();
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
                icon: new FormValidation.plugins.Icon({
                    valid: 'fa fa-check',
                    invalid: 'fa fa-times',
                    validating: 'fa fa-refresh',
                }),
            },
            fields: {
                date_joined: {
                    validators: {
                        notEmpty: {
                            message: 'La fecha es obligatoria'
                        },
                        date: {
                            format: 'YYYY-MM-DD',
                            message: 'La fecha no es válida'
                        },
                        remote: {
                            url: pathname,
                            data: function () {
                                return {
                                    date_joined: fv.form.querySelector('[name="date_joined"]').value,
                                    action: 'validate_data'
                                };
                            },
                            message: 'La fecha de asistencia ya esta registrada',
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
            var assistances = assistance.getAssistances();
            if (assistances.length === 0) {
                message_error('Debe tener al menos un empleado en el listado de asistencias');
                return false;
            }
            parameters.append('assistances', JSON.stringify(assistances));
            submit_formdata_with_ajax('Notificación',
                '¿Estas seguro de realizar la siguiente acción?',
                pathname,
                parameters,
                function () {
                    location.href = fv.form.getAttribute('data-url');
                }
            );
        });
});

$(function () {

    input_date_joined = $('input[name="date_joined"]');

    $('#tblAssistance tbody')
        .off()
        .on('change', 'input[name="state"]', function () {
            var td = tblAssistance.cell($(this).closest('td, li')).index();
            var row = tblAssistance.row(td.row).data();
            row.state = this.checked ? 1 : 0;
            var tr = $(this).parents('tr')[0];
            var background = !this.checked ? '#fff' : '#fff0d7';
            $(tr).css('background', background);
            $('td', tblAssistance.row(tr.row).node()).find('input[type="text"]').prop('disabled', this.checked);
        })
        .on('keyup', 'input[name="details"]', function () {
            var td = tblAssistance.cell($(this).closest('td, li')).index(),
                row = tblAssistance.row(td.row).data();
            row.details = $(this).val();
        });

    $('input[type="checkbox"][name="state_all"]').on('change', function () {
        var state = this.checked;
        if (tblAssistance !== null) {
            var cells = tblAssistance.cells().nodes();
            $(cells).find('input[name="state"]').prop('checked', state).trigger('change');
            $(cells).find('input[name="details"]').prop('disabled', state);
        }
    });

    input_date_joined.datetimepicker({
        useCurrent: false,
        format: 'YYYY-MM-DD',
        locale: 'es',
        keepOpen: false,
        daysOfWeekDisabled: [0]
        //minDate: new moment().format("YYYY-MM-DD")
    });

    input_date_joined.on('change.datetimepicker change.datetimepicker', function (e) {
        fv.validateField('date_joined').then(function (status) {
            if (status === 'Valid') {
                assistance.listAssistances();
            } else if (tblAssistance !== null) {
                tblAssistance.clear().draw();
            }
        });
    });

    input_date_joined.trigger('change');
});

