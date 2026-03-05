var input_year_month;
var current_date;
var select_employee;
var tblReport;
var columns = [];
var report = {
    list: function (all) {
        var parameters = {
            'action': 'search_report',
            'employee': select_employee.val(),
            'year': input_year_month.datetimepicker('date').format("YYYY"),
            'month': input_year_month.datetimepicker('date').format("MM"),
        };

        if (all) {
            parameters['year'] = '';
            parameters['month'] = '';
        }

        tblReport = $('#tblReport').DataTable({
            destroy: true,
            autoWidth: false,
            ajax: {
                url: pathname,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: parameters,
                dataSrc: ''
            },
            order: [[0, 'asc']],
            dom: 'Bfrtip',
            buttons: [
                {
                    extend: 'excelHtml5',
                    text: '<i class="fas fa-file-excel"></i> Descargar Excel',
                    titleAttr: 'Excel',
                    className: 'btn btn-success btn-flat btn-sm'
                },
                {
                    extend: 'pdfHtml5',
                    text: '<i class="fas fa-file-pdf"></i> Descargar Pdf',
                    titleAttr: 'PDF',
                    className: 'btn btn-danger btn-flat btn-sm',
                    title: '',
                    orientation: 'landscape',
                    pageSize: 'LEGAL',
                    download: 'open',
                    customize: function (doc) {
                        doc.styles = {
                            header: {
                                fontSize: 18,
                                bold: true,
                                alignment: 'center'
                            },
                            subheader: {
                                fontSize: 18,
                                bold: true
                            },
                            quote: {
                                italics: true
                            },
                            small: {
                                fontSize: 15
                            },
                            tableHeader: {
                                bold: true,
                                fontSize: 13,
                                color: 'white',
                                fillColor: '#001f3f',
                                alignment: 'center'
                            }
                        };
                        doc.content.splice(0, 0, {
                            margin: [0, 0, 0, 12],
                            fit: [75, 75],
                            alignment: 'center',
                            image: company.image_in_base64
                        });
                        doc.content.splice(1, 0, {
                            text: company.name,
                            style: 'header',
                        });
                        doc.content.splice(2, 0, {
                            alignment: 'center',
                            text: '' + current_date,
                            style: 'subheader'
                        });
                        doc.content.splice(3, 0, {
                            alignment: 'center',
                            text: title,
                            style: 'subheader'
                        });
                        doc.content[4].table.widths = columns;
                        doc.content[4].margin = [0, 35, 0, 0];
                        doc.content[4].layout = {};
                        doc.defaultStyle.fontSize = 13;
                        doc['footer'] = (function (page, pages) {
                            return {
                                columns: [
                                    {
                                        alignment: 'left',
                                        text: ['Fecha de creación: ', {text: current_date.toString()}]
                                    },
                                    {
                                        alignment: 'right',
                                        text: ['página ', {text: page.toString()}, ' de ', {text: pages.toString()}]
                                    }
                                ],
                                margin: 20
                            }
                        });
                    }
                }
            ],
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
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return row.year + '/' + row.month;
                    }
                },
                {
                    targets: [-1, -2, -3, -4, -5, -7, -8],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + data.toFixed(2);
                    }
                },
                {
                    targets: [-6],
                    class: 'text-center',
                },
                {
                    targets: [0],
                    class: 'text-left',
                    render: function (data, type, row) {
                        return row.employee.names + " (" + row.employee.dni + ")";
                    }
                },
            ],
            rowCallback: function (row, data, index) {

            },
            initComplete: function (settings, json) {
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
    },
    initTable: function () {
        tblReport = $('#tblReport').DataTable({
            autoWidth: false,
            destroy: true,
        });
        tblReport.settings()[0].aoColumns.forEach(function (value, index, array) {
            columns.push(value.sWidthOrig);
        });
    }
};

$(function () {

    input_year_month = $('input[name="year_month"]');
    select_employee = $('select[name="employee"]');
    current_date = new moment().format('YYYY-MM-DD');

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es",
    });

    select_employee
        .on('change', function () {
            report.list(false);
        });

    input_year_month.datetimepicker({
        viewMode: 'years',
        format: 'MM/YY',
        useCurrent: false,
        locale: 'es',
        date: new Date(),
    });

    input_year_month.on('hide.datetimepicker change.datetimepicker', function (e) {
        report.list(false);
    });

    $('.btnSearchAll').on('click', function () {
        report.list(true);
    });

    report.initTable();

    report.list(false);
});
