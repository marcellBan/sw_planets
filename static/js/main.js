$(document).ready(function() {
    $('#prev-page').click(pageButtonClick);
    $('#next-page').click(pageButtonClick);
});

function pageButtonClick(){
    var dataUrl = $(this).data('url');
    getTable(dataUrl);
}

function getTable(url) {
    $.ajax({
        url: `/get-table?url=${url}`,
        success: function(result) {
            $('#table-wrapper').html(result);
            $('#prev-page').click(pageButtonClick);
            $('#next-page').click(pageButtonClick);
        }
    });
}
