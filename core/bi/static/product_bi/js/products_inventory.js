var input_year;
var select_product;

var chart = {
    graph: function () {
        var parameters = {
            'action': 'search_report',
            'year': input_year.val(),
            'product': select_product.val(),
        };
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
                            type: 'column'
                        },
                        title: {
                            text: ''
                        },
                        subtitle: {
                            text: ''
                        },
                        exporting: false,
                        xAxis: {
                            categories: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
                            crosshair: true
                        },
                        yAxis: {
                            min: 0,
                            title: {
                                text: ''
                            }
                        },
                        tooltip: {
                            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
                            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                                '<td style="padding:0"><b>{point.y:.0f}</b></td></tr>',
                            footerFormat: '</table>',
                            shared: true,
                            useHTML: true
                        },
                        plotOptions: {
                            column: {
                                pointPadding: 0.2,
                                borderWidth: 0
                            }
                        },
                        series: request
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
    select_product = $('select[name="product"]');
    input_year = $('input[name="year"]');

    $('.select2').select2({
        language: 'es',
        theme: 'bootstrap4',
        width: null
    });

    select_product.on('change', function () {
        chart.graph();
    });

    input_year.datetimepicker({
        locale: 'es',
        keepOpen: true,
        viewMode: 'years',
        format: 'YYYY',
        date: new Date(),
    });

    input_year.keypress(function (e) {
        return validate_form_text('numbers', e, null);
    });

    input_year.on('change.datetimepicker', function (e) {
        chart.graph();
    });

    chart.graph();
});