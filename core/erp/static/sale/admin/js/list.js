var tblSale;
var input_date_range;
var sale = {
    object: null,
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
        tblSale = $('#data').DataTable({
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
            order: [[0, "desc"], [5, "desc"]],
            columns: [
                {data: "number"},
                {data: "client.user.names"},
                {data: "type.name"},
                {data: "date_joined"},
                {data: "subtotal"},
                {data: "total_iva"},
                {data: "total"},
                {data: "status"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-7],
                    class: 'text-center',
                    render: function (data, type, row) {
                        var name = row.type.name;
                        switch (row.type.id) {
                            case "sale":
                                return '<span class="badge badge-primary badge-pill">' + name + '</span>';
                            case "quotation":
                                return '<span class="badge badge-warning badge-pill">' + name + '</span>';
                            case "order":
                                if ($.isEmptyObject(row.voucher)) {
                                    return '<span class="badge badge-info badge-pill">' + name + '</span>';
                                }
                                return '<a href="' + row.voucher + '" target="_blank" class="badge badge-info badge-pill">' + name + '</a>';
                        }
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        var name = row.status.name;
                        switch (row.status.id) {
                            case "dispatched":
                                return '<span class="badge badge-primary badge-pill">' + name + '</span>';
                            case "awaiting_payment":
                                return '<a href="' + row.voucher + '" class="badge badge-warning badge-pill cursor-pointer">' + name + '</a>';
                            case "quoted":
                                return '<span class="badge badge-info badge-pill">' + name + '</span>';
                        }
                    }
                },
                {
                    targets: [-3, -4, -5],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + data.toFixed(2);
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        var buttons = '';
                        buttons += '<a class="btn btn-info btn-xs btn-flat" rel="detail"><i class="fas fa-folder-open"></i></a> ';
                        if (row.status.id === 'awaiting_payment') {
                            buttons += '<a data-toggle="tooltip" title="Subir comprobante" class="btn btn-secondary btn-xs btn-flat" rel="upload_voucher"><i class="fas fa-file-upload"></i></a> ';
                        }
                        buttons += '<a href="' + pathname + 'print/invoice/' + row.id + '/" target="_blank" class="btn btn-primary btn-xs btn-flat"><i class="fas fa-print"></i></a> ';
                        buttons += '<a href="' + pathname + 'delete/' + row.id + '/" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash"></i></a> ';
                        return buttons;
                    }
                },
            ],
            rowCallback: function (row, data, index) {

            },
            initComplete: function (settings, json) {
                $('[data-toggle="tooltip"]').tooltip();
                $(this).wrap('<div class="dataTables_scroll"><div/>');
                var total = json.reduce((a, b) => a + (b.total || 0), 0);
                $('.total').html('$' + total.toFixed(2));
            }
        });
    }
}

$(function () {

    input_date_range = $('input[name="date_range"]');

    $('#data tbody')
        .off()
        .on('click', 'a[rel="detail"]', function () {
            $('.tooltip').remove();
            var tr = tblSale.cell($(this).closest('td, li')).index();
            var row = tblSale.row(tr.row).data();
            $('#tblProducts').DataTable({
                autoWidth: false,
                destroy: true,
                ajax: {
                    url: pathname,
                    type: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                    data: {
                        'action': 'search_detail_products',
                        'id': row.id
                    },
                    dataSrc: ""
                },
                columns: [
                    {data: "product.short_name"},
                    {data: "price"},
                    {data: "cant"},
                    {data: "subtotal"},
                ],
                columnDefs: [
                    {
                        targets: [-1, -3],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return '$' + data.toFixed(2);
                        }
                    },
                    {
                        targets: [-2],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return data;
                        }
                    }
                ],
                initComplete: function (settings, json) {
                    $(this).wrap('<div class="dataTables_scroll"><div/>');
                }
            });
            $('#myModalDetails').modal('show');
        })
        .on('click', 'a[rel="upload_voucher"]', function () {
            $('.tooltip').remove();
            var tr = tblSale.cell($(this).closest('td, li')).index();
            sale.object = tblSale.row(tr.row).data();

            $.ajax({
                url: pathname,
                data: {
                    'action': 'check_available_stock_of_products',
                    'id': sale.object.id
                },
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                dataType: 'json',
                success: function (request) {
                    if (request.hasOwnProperty('error')) {
                        alert_sweetalert('error', 'Alerta', null, function () {

                        }, 2000, request.error);
                        return false;
                    } else {
                        fv.resetForm(true);
                        $('#myModalUploadVoucher').modal('show');
                    }
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    message_error(errorThrown + ' ' + textStatus);
                }
            });
        });

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
            sale.list(false);
        });

    $('.drp-buttons').hide();

    sale.list(false);

    $('.btnSearchAll').on('click', function () {
        sale.list(true);
    });
});
