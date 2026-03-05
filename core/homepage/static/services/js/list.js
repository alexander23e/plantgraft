var services = {
    list: function () {
        var parameters = {
            'action': 'search',
        };
        $('#data').DataTable({
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
            columns: [
                {data: "id"},
                {data: "name"},
                {data: "image"},
                {data: "description_short"},
                {data: "state"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (row.state) {
                            return '<span class="badge badge-success">Activo</span>';
                        }
                        return '<span class="badge badge-danger">Inactivo</span>';
                    }
                },
                {
                    targets: [-4],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<img alt="" src="' + row.image + '" class="img-fluid d-block mx-auto" style="width: 20px; height: 20px;">';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        var buttons = '';
                        buttons += '<a href="' + pathname + 'update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a href="' + pathname + 'delete/' + row.id + '/" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash"></i></a> ';
                        return buttons;
                    }
                },
            ],
            rowCallback: function (row, data, index) {

            },
            initComplete: function (settings, json) {
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
    }
};

$(function () {
    services.list();
});