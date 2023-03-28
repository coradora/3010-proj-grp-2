const rowsPerPage = 10;
var filteredRows = [];


function displayDate(){
    var currentDate = new Date();
    var dateString = currentDate.toLocaleDateString();
    document.getElementById('date-display').textContent = dateString;
}

// Sets a cap of rows a table may display on a given page. 
function paginateTable(page) {
    var start = (page - 1) * rowsPerPage;
    var end = start + rowsPerPage;

    $('table tbody tr').hide();
    for (var i = start; i < end && i < filteredRows.length; i++) {
        $(filteredRows[i]).show();
    }
}


// Filters the table data based on search query
function filterTable() {
    filteredRows = [];
    $('table tbody tr').each(function () {
        var showRow = true;
        $(this).find('td').each(function (index) {
            var searchValue = $('table thead input').eq(index).val().toLowerCase();
            var rowValue = $(this).text().toLowerCase();
            if (rowValue.indexOf(searchValue) === -1) {
                showRow = false;
            }
        });
        if (showRow) {
            filteredRows.push(this);
        }
    });
}


function updatePaginationLinks(currentPage){
    var totalPages = Math.ceil(filteredRows.length / rowsPerPage);

    var maxVisiblePages = 5;
    var firstVisiblePage = Math.max(1, currentPage - Math.floor(maxVisiblePages / 2));
    var lastVisiblePage = Math.min(totalPages, firstVisiblePage + maxVisiblePages - 1);

    // Remove existing pagination links/ellipses except for previous and next buttons.
    $('.pagination .page-link:not(.prev):not(.next)').closest('.page-item').not('.prev, .next').remove();
    $('.pagination .pagination-ellipsis').closest('.page-item').remove();

    // Add pagination links
    for (var i = firstVisiblePage; i <= lastVisiblePage; i++){
        var pageLink = $('<a href="#" class="page-link">' + i + '</a>');
        var pageItem = $('<li class="page-item"></li>');
        pageItem.append(pageLink);
        if(i === currentPage){
            pageItem.addClass('active');
        }

        pageLink.on('click', function(e)
        {
            e.preventDefault();
            var newPage = parseInt($(this).text());
            paginateTable(newPage);
            updatePaginationLinks(newPage);
        });

        $('.pagination .next').closest('.page-item').before(pageItem);
    }

    if(firstVisiblePage > 1) {
        var ellipsis = $('<span class="pagination-ellipsis">&hellip;</span>');
        var ellipsisItem = $('<li class="page-item disabled"></li>');
        ellipsisItem.append(ellipsis);
        $('.pagination .prev').closest('.page-item').after(ellipsisItem);
    }

    if(lastVisiblePage < totalPages) {
        var ellipsis = $('<span class="pagination-ellipsis">&hellip;</span>');
        var ellipsisItem = $('<li class="page-item disabled"></li>');
        ellipsisItem.append(ellipsis);
        $('.pagination .next').closest('.page-item').before(ellipsisItem);
    }
}

$(document).ready(function () {
    displayDate();

    $('table thead th.search').each(function () {
        $(this).html('<input type="text" class="form-control form-control-sm">');
    });

    $('table thead input').on('keyup', function () {
        filterTable();
        paginateTable(1);
        updatePaginationLinks(1);
        //$('.pagination .current-page').text(1);
    });

    // Initialize filteredRows array with current row content
    filterTable()
    paginateTable(1);
    updatePaginationLinks(1);

    $('.pagination-container').on('click', '.pagination .prev', function (e) {
        
        e.preventDefault();
        var currentPage = parseInt($('.pagination .page-item.active .page-link').text());
        if (currentPage > 1) {
            console.log('prev!')
            paginateTable(currentPage - 1);
            updatePaginationLinks(currentPage - 1);
        }
    });

    $('.pagination-container').on('click', '.pagination .next', function(e){
        
        e.preventDefault();
        var currentPage = parseInt($('.pagination .page-item.active .page-link').text());
        var totalPages = Math.ceil(filteredRows.length / rowsPerPage);
        console.log(currentPage)
        if (currentPage < totalPages) {
            paginateTable(currentPage + 1);
            updatePaginationLinks(currentPage + 1);
        }
    });
});

