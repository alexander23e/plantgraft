var fv;
var input_birthdate;

document.addEventListener('DOMContentLoaded', function (e) {
    fv = FormValidation.formValidation(document.getElementById('frmForm'), {
            locale: 'es_ES',
            localization: FormValidation.locales.es_ES,
            plugins: {
                trigger: new FormValidation.plugins.Trigger(),
                submitButton: new FormValidation.plugins.SubmitButton(),
                bootstrap5: new FormValidation.plugins.Bootstrap5({
                    rowSelector: '.mb-3',
                }),
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
                        callback: {
                            message: 'El número de cedula es incorrecto',
                            callback: function (input) {
                                return validate_dni_ruc(input.value);
                            },
                        },
                        remote: {
                            url: pathname,
                            data: function () {
                                return {
                                    parameter: fv.form.querySelector('[name="dni"]').value,
                                    pattern: 'dni',
                                    action: 'validate_data'
                                };
                            },
                            message: 'El número de cédula ya se encuentra registrado',
                            method: 'POST',
                            headers: {
                                'X-CSRFToken': csrftoken
                            },
                        },
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
                                    parameter: fv.form.querySelector('[name="mobile"]').value,
                                    pattern: 'mobile',
                                    action: 'validate_data'
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
                                    parameter: fv.form.querySelector('[name="email"]').value,
                                    pattern: 'email',
                                    action: 'validate_data'
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
            parameters.append('action', 'create_account');
            submit_formdata_with_ajax('Notificación', '¿Estas seguro de registrarse?', pathname, parameters, function () {
                alert_sweetalert('success', 'Alerta', 'Se ha registrado correctamente en nuestro sitio web. Se le ha enviado un correo donde estaran sus credenciales', function () {
                    location.href = fv.form.getAttribute('data-url');
                }, null, null)
            });
        });
});

$(function () {

    input_birthdate = $('input[name="birthdate"]');

    input_birthdate.datetimepicker({
        useCurrent: false,
        format: 'YYYY-MM-DD',
        locale: 'es',
        keepOpen: false,
        maxDate: new Date()
    });

    input_birthdate.datetimepicker('date', moment().format("YYYY-MM-DD"));

    input_birthdate.on('change.datetimepicker', function (e) {
        fv.revalidateField('birthdate');
    });

    $('input[name="names"]').on('keypress', function (e) {
        return validate_form_text('letters', e, null);
    });

    $('input[name="dni"]').on('keypress', function (e) {
        return validate_form_text('numbers', e, null);
    });

    $('input[name="mobile"]').on('keypress', function (e) {
        return validate_form_text('numbers', e, null);
    });

    // $(fv.form).find('input[name="names"]').val('William Jair Dávila Vargas');
    // $(fv.form).find('input[name="dni"]').val('0928363993');
    // $(fv.form).find('input[name="email"]').val('williamjairdavilavargas@gmail.com');
    // $(fv.form).find('input[name="mobile"]').val('0979014551');
    // $(fv.form).find('input[name="address"]').val('Milagro, Ecuador');
});