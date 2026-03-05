var input_year;

var chart = {
    graph: function () {
        var parameters = {
            'action': 'search_report',
            'year': input_year.val()
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
                            type: 'cylinder',
                            options3d: {
                                enabled: true,
                                alpha: 15,
                                beta: 15,
                                depth: 120,
                                viewDistance: 25
                            }
                        },
                        title: {
                            text: ''
                        },
                        subtitle: {
                            text: ''
                        },
                        exporting: false,
                        xAxis: {
                            categories: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
                        },
                        yAxis: {
                            title: {
                                margin: 20,
                                text: ''
                            }
                        },
                        tooltip: {
                            headerFormat: '<b>Age: {point.x}</b><br>'
                        },
                        plotOptions: {
                            series: {
                                depth: 25,
                                colorByPoint: true
                            }
                        },
                        series: [{
                            data: request,
                            name: 'Cantidad',
                            showInLegend: false,
                            dataLabels: {
                                enabled: true,
                                rotation: 0,
                                color: '#FFFFFF',
                                align: 'right',
                                format: '{point.y:.0f}',
                                y: 50,
                                x: -14,
                                style: {
                                    fontSize: '12px',
                                    fontFamily: 'Verdana, sans-serif'
                                }
                            }
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
    input_year = $('input[name="year"]');

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