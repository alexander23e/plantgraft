var fv;
var select_calculation_method;

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
                                    parameter: fv.form.querySelector('[name="name"]').value,
                                    pattern: 'name',
                                    action: 'validate_data'
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
                type: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un item'
                        },
                    }
                },
                calculation_method: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un item'
                        },
                    }
                },
                percent: {
                    validators: {
                        notEmpty: {},
                        numeric: {
                            message: 'El valor no es un número',
                            thousandsSeparator: '',
                            decimalSeparator: '.'
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
            submit_formdata_with_ajax_form(fv);
        });
});

$(function () {

    select_calculation_method = $('select[name="calculation_method"]');

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es",
    });

    $('select[name="type"]')
        .on('change.select2', function () {
            fv.revalidateField('type');
        });

    select_calculation_method
        .on('change', function () {
            var container = $(this).parent().parent().find('input[name="percent"]').parent().parent();
            $(container).show();
            if ($(this).val() === 'amount') {
                $(container).hide();
            }
        });

    $('[name="percent"]').TouchSpin({
        min: 0.00,
        max: 100000,
        step: 0.01,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
    })
        .on('keypress', function (e) {
            return validate_decimals($(this), e);
        });

    $('input[name="name"]').on('keypress', function (e) {
        return validate_form_text('letters', e, null);
    });

    select_calculation_method.trigger('change');

    $('i[data-field="percent"]').hide();
});
