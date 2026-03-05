var input_year;
var select_client;

var chart = {
    graph: function () {
        var parameters = {
            'action': 'search_report',
            'year': input_year.val(),
            'client': JSON.stringify(select_client.select2('data').map(value => value.id)),
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
                            type: 'spline'
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
                            accessibility: {
                                description: ''
                            }
                        },
                        yAxis: {
                            title: {
                                text: ''
                            },
                        },
                        tooltip: {
                            formatter() {
                                const chart = this;
                                return `<b>${chart.x}</b><br />${chart.points
                                    .sort((pointA, pointB) => pointB.y - pointA.y)
                                    .map((point) => {
                                        return `<span style="color: ${point.color}">\u25CF</span> ${point.series.name}: ${point.y}`;
                                    })
                                    .join("<br />")}`;
                            },
                            crosshairs: true,
                            shared: true,
                        },
                        plotOptions: {
                            spline: {
                                marker: {
                                    radius: 4,
                                    lineColor: '#666666',
                                    lineWidth: 1
                                }
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
    input_year = $('input[name="year"]');
    select_client = $('select[name="clients"]');

    $('.select2').select2({
        placeholder: 'Buscar..',
        language: 'es',
        theme: 'bootstrap4',
        width: null
    });

    select_client.on('select2:close', function () {
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

    $('.btnSelectAll').on('click', function () {
        select_client.find('option').prop('selected', 'selected').end().trigger('change').trigger('select2:close');
    });

    $('.btnRemoveAll').on('click', function () {
        select_client.val('').trigger('change').trigger('select2:close');
    });

    chart.graph();
});