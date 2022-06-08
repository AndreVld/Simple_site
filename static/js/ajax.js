$(document).ready(function () {
    $('.worksBx').on('click', 'input[type="button"]', function () {

        $.ajax({
            url: '/read_post/'+ this.name + '/',
            type: "GET",
            success: function (response) {
                $('.popupBx').html(response.result);
                    modal();
            },
            error: function (response) {
                      alert(response.responseJSON.errors);
                  }
        });
        event.preventDefault();
    });

})