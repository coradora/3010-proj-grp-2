// Displays the current date on the navbar
function displayDate() {
    var currentDate = new Date();
    var dateString = currentDate.toLocaleDateString();
    document.getElementById('date-display').textContent = dateString;
}

// Updates the active link on the navbar
function updateActive() {
    var pathname = window.location.pathname;
    pathname = pathname.slice(1);
    $("#" + pathname).addClass("active");
}

$(document).ready(function () {
    // Calls displayDate and updateActive
    displayDate();
    updateActive();

    // Setup DataTable - add a text input to each footer cell
    $('#csdashboard thead tr')
        .clone(true)
        .addClass('filters')
        .appendTo('#csdashboard thead');

    var table = $('#csdashboard').DataTable({
        orderCellsTop: true,
        fixedHeader: true,
        "order": [], // ignore default DataTable ordering
        "searching": true,
        "ordering": true,
        // DOM control elements - 'l' enables length input control
        // 'r' enables processing display element, 't' enables table, 
        // 'i' enables table info, 'p' enables pagination. 
        // Useful for disabling certain visual elements but keeping functionality
        dom: 'lrtip',
        initComplete: function () {
            var api = this.api();

            // For each column
            api
                .columns()
                .eq(0)
                .each(function (colIdx) {
                    // Set the header cell to contain the input element
                    var cell = $('.filters th').eq(
                        $(api.column(colIdx).header()).index()
                    );
                    var title = $(cell).text();
                    $(cell).html('<input type="text"' + title + '" style="width: 75%;"/>');

                    // On every keypress in this input
                    $(
                        'input',
                        $('.filters th').eq($(api.column(colIdx).header()).index())
                    )
                        .off('keyup change')
                        .on('change', function (e) {
                            // Get the search value
                            $(this).attr('title', $(this).val());
                            var regexr = '({search})'; //$(this).parents('th').find('select').val();

                            var cursorPosition = this.selectionStart;
                            // Search the column for that value
                            api
                                .column(colIdx)
                                .search(
                                    this.value != ''
                                        ? regexr.replace('{search}', '(((' + this.value + ')))')
                                        : '',
                                    this.value != '',
                                    this.value == ''
                                )
                                .draw();
                        })
                        .on('keyup', function (e) {
                            e.stopPropagation();

                            $(this).trigger('change');
                            $(this)
                                .focus()[0]
                                .setSelectionRange(cursorPosition, cursorPosition);
                        });
                });
        },
    });
});
