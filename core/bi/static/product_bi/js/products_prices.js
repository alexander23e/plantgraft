var chart = {
    graph: function () {
        var parameters = {
            'action': 'search_report',
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
                            pointFormat: 'Precio: <b>{point.y:.2f}</b>'
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
                                align: 'center',
                                format: '{point.y:.2f}',
                                y: 50,
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
    chart.graph();
});