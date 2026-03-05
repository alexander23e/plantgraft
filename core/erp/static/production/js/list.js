var tblProduction;
var input_date_range;
var production = {
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
        tblProduction = $('#data').DataTable({
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
            order: [[0, 'desc']],
            columns: [
                {data: "id"},
                {data: "lot.name"},
                {data: "start_date"},
                {data: "end_date"},
                {data: "state"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (row.state) {
                            return '<a rel="finish_production" class="btn btn-secondary btn-xs btn-flat"><i class="fas fa-truck-monster"></i> Finalizar</a>'
                        }
                        return data;
                    }
                },
                {
                    targets: [-4, -5],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return data;
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (data) {
                            return '<span class="badge badge-success badge-pill">Activo</span>';
                        }
                        return '<span class="badge badge-danger badge-pill">Inactivo</span>';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        var buttons = '';
                        buttons += '<a class="btn btn-success btn-xs btn-flat" rel="detail"><i class="fas fa-folder-open"></i></a> ';
                        buttons += '<a data-toggle="tooltip" title="Ver etapa de crecimiento" href="' + pathname + 'stages/' + row.id + '/" class="btn btn-primary btn-xs btn-flat"><i class="fa-solid fa-book-bookmark"></i></a> ';
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
            production.list(false);
        });

    $('.drp-buttons').hide();

    production.list(false);

    $('.btnSearchAll').on('click', function () {
        production.list(true);
    });

    $('#data tbody')
        .off()
        .on('click', 'a[rel="detail"]', function () {
            $('.tooltip').remove();
            var tr = tblProduction.cell($(this).closest('td, li')).index(),
                row = tblProduction.row(tr.row).data();
            $('#tblResources').DataTable({
                autoWidth: false,
                destroy: true,
                ajax: {
                    url: pathname,
                    type: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                    data: {
                        'action': 'search_detail_resources',
                        'id': row.id
                    },
                    dataSrc: ""
                },
                columns: [
                    {data: "resource.code"},
                    {data: "resource.name"},
                    {data: "resource.category.name"},
                    {data: "cant"},
                ],
                columnDefs: [
                    {
                        targets: [-1],
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
                    {data: "product.id"},
                    {data: "product.name"},
                    {data: "product.type.name"},
                    {data: "cant"},
                ],
                columnDefs: [
                    {
                        targets: [-2],
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
                        targets: [-1],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return data;
                        }
                    },
                ],
                initComplete: function (settings, json) {
                    $(this).wrap('<div class="dataTables_scroll"><div/>');
                }
            });
            $('.nav-tabs a[href="#home"]').tab('show');
            $('#myModalDetails').modal('show');
        })
        .on('click', 'a[rel="finish_production"]', function () {
            $('.tooltip').remove();
            var tr = tblProduction.cell($(this).closest('td, li')).index(),
                row = tblProduction.row(tr.row).data();
            submit_with_ajax('Alerta', '¿Estas seguro de finalizar la producción?', pathname, {
                'action': 'finish_production',
                'id': row.id,
            }, function () {
                tblProduction.ajax.reload();
            })
        });

    $('#data').addClass('table-sm');
});