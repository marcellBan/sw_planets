$(document).ready(function() {
    $('#prev-page').click(pageButtonClick);
    $('#next-page').click(pageButtonClick);
    $('.residents-modal-activator').click(loadModalData);
    $('#residents-modal').on('shown.bs.modal', function(){
        $('#residents-modal .modal-body').height($('#residents-modal table').height());
        $(this).css('opacity', '1');
        $('#residents-modal .modal-dialog').css('transform', '');
    });
});

function loadModalData(event) {
    var url = $(this).data('purl');
    $('#residents-modal .modal-content').load(`/get-modal-content?url=${url}`, function(){
        $('#residents-modal').modal('show');
        $('#residents-modal').css('opacity', '0');
        $('#residents-modal .modal-dialog').css('transform', 'translate(0,-25%)');
    });
}

function pageButtonClick() {
    var dataUrl = $(this).data('url');
    getTable(dataUrl);
}

function getTable(url) {
    $('#table-wrapper').load(`/get-table?url=${url}`, function(){
        $('#prev-page').click(pageButtonClick);
        $('#next-page').click(pageButtonClick);
        $('.residents-modal-activator').click(loadModalData);
    });
}
