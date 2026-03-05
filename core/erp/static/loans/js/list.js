var input_date_range;
var tblLoans, tblPayments;
var loans = {
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
        tblLoans = $('#data').DataTable({
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: pathname,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: parameters,
                dataSrc: ""
            },
            columns: [
                {data: "id"},
                {data: "date_joined"},
                {data: "employee.names"},
                {data: "employee.dni"},
                {data: "valor"},
                {data: "quota"},
                {data: "role_discount"},
                {data: "saldo"},
                {data: "state"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-5],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<span class="badge badge-secondary badge-pill">' + data + '</span>';
                    }
                },
                {
                    targets: [-3, -4, -6],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + data.toFixed(2);
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (data) {
                            return '<span class="badge badge-success">Activo</span>';
                        }
                        return '<span class="badge badge-danger">Inactivo</span>';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        var buttons = '';
                        buttons += '<a rel="detail" class="btn btn-primary btn-xs btn-flat"><i class="fa-solid fa-magnifying-glass-dollar"></i></a> ';
                        buttons += '<a href="' + pathname + 'delete/' + row.id + '/" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash"></i></a> ';
                        return buttons;
                    }
                },
            ],
            rowCallback: function (row, data, index) {

            },
            initComplete: function (settings, json) {
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
    }
};

$(function () {
    input_date_range = $('input[name="date_range"]');

    input_date_range
        .daterangepicker({
                language: 'auto',
                startDate: new Date(),
                locale: {
                    format: 'YYYY-MM-DD',
                },
                autoApply: true,
            }
        )
        .on('change.daterangepicker apply.daterangepicker', function (ev, picker) {
            loans.list(false);
        });

    $('.drp-buttons').hide();

    loans.list(false);

    $('.btnSearchAll').on('click', function () {
        loans.list(true);
    });

    $('#data tbody')
        .off()
        .on('click', 'a[rel="detail"]', function () {
            $('.tooltip').remove();
            var tr = tblLoans.cell($(this).closest('td, li')).index(),
                row = tblLoans.row(tr.row).data();
            tblPayments = $('#tblPayments').DataTable({
                autoWidth: false,
                destroy: true,
                ajax: {
                    url: pathname,
                    type: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                    data: {
                        'action': 'search_detail_payments',
                        'id': row.id
                    },
                    dataSrc: ""
                },
                columns: [
                    {data: "date_joined"},
                    {data: "salary"},
                    {data: "valor"},
                    {data: "id"},
                ],
                columnDefs: [
                    {
                        targets: [-2],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return '$' + data.toFixed(2);
                        }
                    },
                    {
                        targets: [-3],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return row.salary.year + '/' + row.salary.month;
                        }
                    },
                    {
                        targets: [-1],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return '<a rel="delete" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash"></i></a>';
                        }
                    }
                ],
                initComplete: function (settings, json) {
                    $(this).wrap('<div class="dataTables_scroll"><div/>');
                }
            });
            $('#myModalPayments').modal('show');
        });

    $('#tblPayments tbody')
        .off()
        .on('click', 'a[rel="delete"]', function () {
            $('.tooltip').remove();
            var tr = tblPayments.cell($(this).closest('td, li')).index(),
                row = tblPayments.row(tr.row).data();
            submit_with_ajax('Notificación',
                '¿Estas seguro de eliminar el registro?',
                pathname,
                {
                    'id': row.id,
                    'action': 'delete_pay'
                },
                function () {
                    tblPayments.ajax.reload();
                }
            );
        });

    $('#myModalPayments').on('hidden.bs.modal', function () {
        tblLoans.ajax.reload();
    });

});