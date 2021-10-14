




console.log('loaded')

const validateEmail = function(email) {

    console.log('email', email)
    var formData = new FormData();
    formData.append('email', email)
    $.ajaxSetup({
        headers: {
            "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
        }
    });
    $.ajax({
        url: '/validate/',
        type: 'POST',
        dataType: 'json',
        cache: false,
        processData: false,
        contentType: false,
        data: formData,
        error: function (xhr) {
            console.log(xhr)
            console.error(xhr.statusText);
        },
        success: function (res) {
            console.log(res)
            $('.error').text(res.msg);
        }
    });
};
$(document).ready(function(){
    $('#userEmail').change(function(){
        // var email = $('#userEmail').val();
        // console.log('email', email)
        // console.log('this', )
        validateEmail($(this).val())

    });
});



 // $(function() {
 //        setInterval("validateEmail()", 1000);
 //    });

