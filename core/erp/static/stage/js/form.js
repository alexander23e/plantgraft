var fv;

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
                step: {
                    validators: {
                        notEmpty: {},
                        digits: {},
                        remote: {
                            url: pathname,
                            data: function () {
                                return {
                                    parameter: fv.form.querySelector('[name="step"]').value,
                                    pattern: 'step',
                                    action: 'validate_data'
                                };
                            },
                            message: 'El número de paso ya se encuentra registrado',
                            method: 'POST',
                            headers: {
                                'X-CSRFToken': csrftoken
                            },
                        }
                    },
                },
                color: {
                    validators: {
                        notEmpty: {},
                    },
                },
                name: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
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
                description: {
                    validators: {
                        // notEmpty: {},
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
    $('input[name="step"]').on('keypress', function (e) {
        return validate_form_text('numbers', e, null);
    });

    $('input[name="color"]').colorpicker()
        .on('colorpickerChange colorpickerCreate', function (e) {
            fv.revalidateField('color');
        })
        .on('keyup', function () {
            $(this).colorpicker('setValue', $(this).val());
        });

    $('input[name="percent"]')
        .TouchSpin({
            min: 0.00,
            max: 100,
            step: 0.01,
            decimals: 2,
            boostat: 5,
            maxboostedstep: 10,
            prefix: '%'
        })
        .on('change touchspin.on.min touchspin.on.max', function () {
            fv.revalidateField('percent');
        })
        .on('keypress', function (e) {
            return validate_decimals($(this), e);
        });

    $('i[data-field="percent"]').hide();
});