var btnRemoveAssist, btnUpdateAssist;
var current_date;
var tblAssistance;
var input_date_range;
var assistance = {
    list: function (all) {
        var parameters = {
            'action': 'search',
            'start_date': input_date_range.data('daterangepicker').startDate.format('YYYY-MM-DD'),
            'end_date': input_date_range.data('daterangepicker').endDate.format('YYYY-MM-DD'),
        };
        if (all) {
            parameters['start_date'] = '';
            parameters['end_date'] = '';
        }
        tblAssistance = $('#data').DataTable({
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: parameters,
                dataSrc: "",
            },
            columns: [
                {data: "date_joined"},
                {data: "employee.names"},
                {data: "employee.dni"},
                {data: "state"},
                {data: "details"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (row.state) {
                            return '<span class="badge badge-success badge-pill">Si</span>';
                        }
                        return '<span class="badge badge-danger badge-pill">No</span>';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    }
                },
            ],
            initComplete: function (settings, json) {
                 $(this).wrap('<div class="dataTables_scroll"><div/>');
                btnRemoveAssist.prop('disabled', $.isEmptyObject(json));
                if (!all) {
                    btnUpdateAssist.prop('disabled', parameters.start_date !== parameters.end_date || $.isEmptyObject(json));
                } else {
                    btnUpdateAssist.prop('disabled', true);
                }
            }
        });
    }
};

$(function () {

    current_date = moment().format("YYYY-MM-DD");
    input_date_range = $('input[name="date_range"]');
    btnRemoveAssist = $('.btnRemoveAssist');
    btnUpdateAssist = $('.btnUpdateAssist');

    btnRemoveAssist.prop('disabled', true);

    input_date_range
        .daterangepicker({
            language: 'auto',
            startDate: new Date(),
            locale: {
                format: 'YYYY-MM-DD',
            },
            autoApply: true,
        })
        .on('change.daterangepicker apply.daterangepicker', function (ev, picker) {
            assistance.list(false);
        });

    $('.drp-buttons').hide();

    $('.btnSearchAssist').on('click', function () {
        assistance.list(false);
    });

    btnRemoveAssist.on('click', function () {
        location.href = pathname + 'delete/' + input_date_range.data('daterangepicker').startDate.format('YYYY-MM-DD') + '/' + input_date_range.data('daterangepicker').endDate.format('YYYY-MM-DD') + '/';
    });

    btnUpdateAssist.on('click', function () {
        location.href = pathname + 'update/' + input_date_range.data('daterangepicker').startDate.format('YYYY-MM-DD') + '/';
    });

    $('.btnSearchAll').on('click', function () {
        assistance.list(true);
    });

    assistance.list(false);

    // $('#data').addClass('table-sm');

    $('#data tbody')
        .off()
        .on('click', 'a[rel="remove"]', function () {
            $('.tooltip').remove();
            var tr = tblAssistance.cell($(this).closest('td, li')).index(),
                row = tblAssistance.row(tr.row).data();
            submit_with_ajax('Alerta', '¿Estas seguro de eliminar la siguiente asistencia?', pathname, {
                'action': 'remove_assistance',
                'id': row.id,
            }, function () {
                alert_sweetalert('success', 'Alerta', 'Asistencia eliminada', function () {
                    tblAssistance.ajax.reload();
                }, 2000, null);
            })
        });
});
