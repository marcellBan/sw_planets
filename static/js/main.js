$(document).ready(function() {
    var locationArray = window.location.href.split('/');
    var registerPage = false;
    for (let part of locationArray) {
        if (part === "register") {
            registerPage = true;
        }
    }
    if (registerPage) {
        initRegisterPage();
    } else {
        initTablePage();
    }
    $('.flashed-message').slideDown(750).fadeIn(750);
    setTimeout(function() {
        $('.flashed-message').slideUp(750).fadeOut(750);
    }, 2000);
});

function initTablePage() {
    attachTableListeners();
    $('#residents-modal').on('shown.bs.modal', function() {
        $('#residents-modal .modal-body').height($('#residents-modal table').height());
        $(this).css('opacity', '1');
        $('#residents-modal .modal-dialog').css('transform', '');
    });
}

function initRegisterPage() {
    $('#username').focusout(function() {
        var username = $(this).val();
        $.ajax({
            url: `/check-user?username=${username}`,
            success: function(response) {
                if (response === "True") {
                    $('#username').parents('.form-group').addClass('has-error');
                    $('#username').parents('.form-group').removeClass('has-success');
                } else {
                    $('#username').parents('.form-group').addClass('has-success');
                    $('#username').parents('.form-group').removeClass('has-error');
                }
            }
        });
    });
    $('#password-verify').keyup(function() {
        if ($(this).val() !== $('#password').val()) {
            $(this).parents('.form-group').addClass('has-error');
            $(this).parents('.form-group').removeClass('has-success');
        } else {
            $(this).parents('.form-group').addClass('has-success');
            $(this).parents('.form-group').removeClass('has-error');
        }
    });
}

function attachTableListeners() {
    $('#prev-page').click(pageButtonClick);
    $('#next-page').click(pageButtonClick);
    $('.residents-modal-activator').click(loadModalData);
}

function loadModalData(event) {
    var button = $(this);
    var oldText = button.html();
    button.html('Loading...');
    var url = button.data('purl');
    $('#residents-modal .modal-content').load(`/get-modal-content?url=${url}`, function() {
        $('#residents-modal').modal('show').css('opacity', '0');
        $('#residents-modal .modal-dialog').css('transform', 'translate(0,-25%)');
        button.html(oldText);
    });
}

function pageButtonClick() {
    var dataUrl = $(this).data('url');
    $('#content-wrapper').load(`/get-table?url=${dataUrl}`, function() {
        attachTableListeners();
    });
}