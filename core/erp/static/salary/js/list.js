var input_year_month;
var btnRemoveSalary, btnUpdateSalary;
var tblSalary;
var salary = {
    list: function (all) {
        var parameters = {
            'action': 'search',
            'year': input_year_month.datetimepicker('date').format("YYYY").toString(),
            'month': input_year_month.datetimepicker('date').format("MM").toString(),
        };
        if (all) {
            parameters['year'] = '';
            parameters['month'] = '';
        }
        tblSalary = $('#data').DataTable({
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
                {"data": "id"},
                {"data": "employee.names"},
                {"data": "rmu_contract"},
                {"data": "salary_by_day"},
                {"data": "days_work"},
                {"data": "rmu_month"},
                {"data": "ingress"},
                {"data": "egress"},
                {"data": "loan_discount"},
                {"data": "total"},
                {"data": "id"},
            ],
            order: [[0, "asc"]],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return row.year + '/' + row.month;
                    }
                },
                {
                    targets: [-2, -3, -4, -5, -6, -8, -9],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + data.toFixed(2);
                    }
                },
                {
                    targets: [-7],
                    class: 'text-center',
                },
                {
                    targets: [0],
                    class: 'text-left',
                    render: function (data, type, row) {
                        return row.contract.employee.names + " (" + row.contract.employee.dni + ")";
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        var buttons = '<a href="' + pathname + 'print/receipt/' + row.id + '/" target="_blank" class="btn btn-danger btn-flat btn-xs"><i class="fas fa-file-pdf"></i></a> ';
                        buttons += '<a rel="detail" class="btn bg-navy btn-flat btn-xs"><i class="fas fa-dollar-sign"></i></a>';
                        return buttons;
                    }
                },
            ],
            initComplete: function (settings, json) {
                $(this).wrap('<div class="dataTables_scroll"><div/>');
                btnRemoveSalary.prop('disabled', $.isEmptyObject(json));
                btnUpdateSalary.prop('disabled', $.isEmptyObject(json));
            }
        });
    }
};

$(function () {

    btnRemoveSalary = $('.btnRemoveSalary');
    btnUpdateSalary = $('.btnUpdateSalary');
    input_year_month = $('input[name="year_month"]');

    input_year_month.datetimepicker({
        viewMode: 'years',
        format: 'MM/YY',
        useCurrent: false,
        locale: 'es',
        date: new Date(),
    });

    input_year_month.on('hide.datetimepicker change.datetimepicker', function (e) {
        salary.list(false);
    });

    btnRemoveSalary.on('click', function () {
        location.href = pathname + 'delete/' + input_year_month.datetimepicker('date').format("YYYY") + '/' + input_year_month.datetimepicker('date').format("MM") + '/';
    });

    btnUpdateSalary.on('click', function () {
        location.href = pathname + 'update/' + input_year_month.datetimepicker('date').format("YYYY") + '/' + input_year_month.datetimepicker('date').format("MM") + '/';
    });

    $('#data tbody')
        .off()
        .on('click', 'a[rel="detail"]', function () {
            $('.tooltip').remove();
            var td = tblSalary.cell($(this).closest('td, li')).index(),
                row = tblSalary.row(td.row).data();
            $('#tblIngress').DataTable({
                autoWidth: false,
                destroy: true,
                paging: false,
                ajax: {
                    url: pathname,
                    type: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                    data: {
                        'action': 'search_headings',
                        'type': 'ingress',
                        'id': row.id,
                    },
                    dataSrc: ""
                },
                columns: [
                    {"data": "heading_name"},
                    {"data": "valor"},
                    {"data": "total"},
                ],
                columnDefs: [
                    {
                        targets: [-2],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return data.toFixed(2);
                        }
                    },
                    {
                        targets: [-1],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return '$' + data.toFixed(2);
                        }
                    },
                ],
                initComplete: function (settings, json) {
                    $(this).wrap('<div class="dataTables_scroll"><div/>');
                }
            });
            $('#tblEgress').DataTable({
                autoWidth: false,
                destroy: true,
                paging: false,
                ajax: {
                    url: pathname,
                    type: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                    data: {
                        'action': 'search_headings',
                        'type': 'egress',
                        'id': row.id,
                    },
                    dataSrc: ""
                },
                columns: [
                    {"data": "heading_name"},
                    {"data": "valor"},
                    {"data": "total"},
                ],
                columnDefs: [
                    {
                        targets: [-2],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return data.toFixed(2);
                        }
                    },
                    {
                        targets: [-1],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return '$' + data.toFixed(2);
                        }
                    },
                ],
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
                        'id': row.id,
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

    salary.list(false);

    $('.btnSearchAll').on('click', function () {
        salary.list(true);
    });
});