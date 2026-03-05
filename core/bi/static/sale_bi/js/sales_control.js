var input_year;
var select_month;

var chart = {
    graph: function () {
        var parameters = {
            'action': 'search_report',
            'year': input_year.val(),
            'month': select_month.val()
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
                    Highcharts.chart('chart1', {
                        title: {
                            text: ''
                        },
                        subtitle: {
                            text: ''
                        },
                        exporting: false,
                        xAxis: {
                            categories: request.categories
                        },
                        yAxis: {
                            min: 0,
                            title: {
                                text: ''
                            }
                        },
                        tooltip: {
                            pointFormat: 'Total: <b>{point.y:.2f}</b>'
                        },
                        series: [{
                            type: 'column',
                            colorByPoint: true,
                            data: request.series,
                            showInLegend: false,
                            dataLabels: {
                                enabled: true,
                                rotation: 0,
                                color: '#FFFFFF',
                                align: 'right',
                                format: '{point.y:.2f}',
                                y: 50,
                                style: {
                                    fontSize: '11px',
                                    fontFamily: 'Verdana, sans-serif'
                                }
                            }
                        }]
                    });
                    Highcharts.chart('chart2', {
                        chart: {
                            type: 'gauge',
                            plotBackgroundColor: null,
                            plotBackgroundImage: null,
                            plotBorderWidth: 0,
                            plotShadow: false,
                            height: '80%'
                        },
                        title: {
                            text: ''
                        },
                        exporting: false,
                        pane: {
                            startAngle: -90,
                            endAngle: 89.9,
                            background: null,
                            center: ['50%', '75%'],
                            size: '100%'
                        },
                        yAxis: {
                            min: 0,
                            max: 1000000,
                            tickPixelInterval: 72,
                            tickPosition: 'inside',
                            tickColor: Highcharts.defaultOptions.chart.backgroundColor || '#FFFFFF',
                            tickLength: 20,
                            tickWidth: 2,
                            minorTickInterval: null,
                            labels: {
                                distance: 20,
                                style: {
                                    fontSize: '14px'
                                }
                            },
                            plotBands: [{
                                from: 0,
                                to: 5000,
                                color: '#fa8104', // green
                                thickness: 20
                            }, {
                                from: 5000,
                                to: 15000,
                                color: '#DDDF0D', // yellow
                                thickness: 20
                            }, {
                                from: 15000,
                                to: 1000000,
                                color: '#55BF3B', // red
                                thickness: 20
                            }]
                        },
                        series: [{
                            name: 'Total',
                            data: [request.total],
                            tooltip: {
                                valueSuffix: ' $'
                            },
                            dataLabels: {
                                format: '${y}',
                                borderWidth: 0,
                                color: (
                                    Highcharts.defaultOptions.title &&
                                    Highcharts.defaultOptions.title.style &&
                                    Highcharts.defaultOptions.title.style.color
                                ) || '#333333',
                                style: {
                                    fontSize: '16px'
                                }
                            },
                            dial: {
                                radius: '80%',
                                backgroundColor: 'gray',
                                baseWidth: 12,
                                baseLength: '0%',
                                rearLength: '0%'
                            },
                            pivot: {
                                backgroundColor: 'gray',
                                radius: 6
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
    select_month = $('select[name="month"]');

    $('.select2').select2({
        language: 'es',
        theme: 'bootstrap4',
        width: null
    });

    select_month.on('change', function () {
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