var input_date_range;
var select_product_options;

var chart = {
    graph: function (all) {
        var parameters = {
            'action': 'search_report',
            'option': select_product_options.val(),
            'start_date': input_date_range.data('daterangepicker').startDate.format('YYYY-MM-DD'),
            'end_date': input_date_range.data('daterangepicker').endDate.format('YYYY-MM-DD'),
        };
        if (all) {
            parameters['start_date'] = '';
            parameters['end_date'] = '';
        }
        $.ajax({
            url: pathname,
            data: parameters,
            type: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            dataType: 'json',
            beforeSend: function () {
                loading_image('/static/img/default/powerbi.png');
            },
            success: function (request) {
                if (!request.hasOwnProperty('error')) {
                    Highcharts.chart('chart', {
                        chart: {
                            type: 'pie',
                            options3d: {
                                enabled: true,
                                alpha: 45
                            }
                        },
                        exporting: false,
                        title: {
                            text: ''
                        },
                        tooltip: {
                            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
                        },
                        accessibility: {
                            point: {
                                valueSuffix: '%'
                            }
                        },
                        plotOptions: {
                            pie: {
                                innerSize: 100,
                                depth: 45,
                                allowPointSelect: true,
                                cursor: 'pointer',
                                dataLabels: {
                                    enabled: true,
                                    format: '<b>{point.name}</b>: {point.y} ({point.percentage:.1f} %)'
                                }
                            }
                        },
                        series: [{
                            name: 'Porcentaje',
                            colorByPoint: true,
                            data: request
                        }]
                    });
                    return false;
                }
                message_error(request.error);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                message_error(errorThrown + ' ' + textStatus);
            },
            complete: function () {
                $.LoadingOverlay("hide");
            }
        });
    }
};

$(function () {
    select_product_options = $('select[name="product_options"]');
    input_date_range = $('input[name="date_range"]');

    $('.select2').select2({
        language: 'es',
        theme: 'bootstrap4',
    });

    select_product_options.on('change', function () {
        chart.graph(false);
    });

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
            chart.graph(false);
        });

    $('.btnSearchAll').on('click', function () {
        chart.graph(true);
    });

    chart.graph(false);
});