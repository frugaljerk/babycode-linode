const confirmBtn = document.getElementById('confirm-btn')
const imageForm = document.getElementById('image-form')
const csrf = document.getElementsByName('csrfmiddlewaretoken')
const alertBox = document.getElementById('alert-box')

const fd = new FormData(imageForm)

// to valid if user fill all the form fields
var $length = parseInt($('#form-length').text());
var blobDone = parseInt($('#form-length').text());

fd.append('csrfmiddlewaretoken', csrf[0].value)

//identify form input field and initial cropper
$("input:file").click(function(){

    myCroppers(document.getElementById(this.id), document.getElementById(this.name))
    if ($length > 0){
        $length = $length - 1;
    }

    console.log('length', $length)
})




var mode = $('#toggle-event').is(':checked') //true: machinecode, false: hand drawn
console.log('mode', mode)

$(function() {
    $('#toggle-event').change(function() {
        if (mode == true){
            mode = false;
        }else{
            mode = true;
        }
        console.log(mode)
    })
})






//initiate cropping function after form button clicked
function myCroppers(input, imageBox){

    input.addEventListener('change', ()=>{
        alertBox.innerHTML = ""
        // confirmBtn.classList.remove('not-visible')
        const img_data = input.files[0]
        const url = URL.createObjectURL(img_data)
        imageBox.innerHTML = `<img src="${url}" id="cropping${imageBox.id}" >`
        console.log(imageBox.id)
        // Adaptive cropbox to character image width and height
        var x = $('#width' + imageBox.id).text();
        var y = $('#height' + imageBox.id).text();

        var $image = $('#cropping'+imageBox.id)
        $image.cropper({
        preview: '#preview1',  //DOTO: ADD PREVIEW
        aspectRatio: x / y,
        crop: function(event) {
            console.log(event.detail.x);
            console.log(event.detail.y);
            console.log(event.detail.width);
            console.log(event.detail.height);
            console.log(event.detail.rotate);
            console.log(event.detail.scaleX);
            console.log(event.detail.scaleY);
        }
    });


    var cropper = $image.data('cropper');

        //initiate blobbing(ie attach blobs to form input)
        confirmBtn.addEventListener('click', ()=>{
            console.log('blobing starts on', input.name)
            cropper.getCroppedCanvas().toBlob((blob) => {
                fd.append(input.name, blob, 'crop.png')
            })
            if (blobDone > 0){
                blobDone = blobDone - 1;
            }

            console.log('finishing blobbing', blobDone)

        })

    })
}

//set timer to delay ajax while blobbing happens
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
//delayed Ajax and check promises before sending
async function delayedAjax() {
    console.log('Waiting for Blobing...');
    await sleep(1500);
    console.log('Two seconds later, showing sleep in a loop...?');
    // Sleep in loop
    // for (let i = 0; i < 5; i++) {if (i === 3)
    //     await sleep(2000);
    //     console.log(i);
    //     }

    let myPromise = new Promise(function(myResolve, myReject){
        console.log('Checking if Promise resolved')
        if (blobDone == 0) {
            console.log('Promoise Resolved')
            myResolve(fd);
            } else {
                myReject("PROMOISE Error");
            }
        });
    myPromise.then(
        function(value) {
            console.log(mode)
            // Set form url according to user input (machine vs hand drawn)
            if (mode == true){
                var action_url = imageForm.action;
                var redirect_url = $("#js-url-machine").attr("data-url");
            }else{
                var action_url = $("#js-url").attr("data-url");
                var redirect_url = $("#js-url-human").attr("data-url");
            }
            console.log('action url', action_url);

            console.log('redirect url', redirect_url);

             $.ajax({
                    type:'POST',
                    // url: imageForm.action,
                    url: action_url,
                    enctype: 'multipart/form-data',
                    data: value,
                    success: function(){
                        // location.reload();
                        window.location.href= redirect_url;
                        console.log('success')
                        alertBox.innerHTML = `<div class="alert alert-success" role="alert">
                                                Successfully saved and cropped the selected image
                                            </div>`
                    },
                    error: function(error){
                        console.log('error', error)
                        alertBox.innerHTML = `<div class="alert alert-danger" role="alert">
                                                Ups...something went wrong
                                            </div>`
                    },
                    cache: false,
                    contentType: false,
                    processData: false,
                })
            console.log('Ajax Complete')
        },

        function(error){
            console.log(error)
        }
    );


}



//click confirmed button to initiate sending
$('#confirm-btn').click(function() {
    if($length == 0){
        console.log('validated')
        delayedAjax();
    }else{
       $('#alert-box').html('Please upload images to all the fields').slideDown();
    }

  // Handler for .ready() called.
});

$('#alert-box').click(function(){
    $(this).slideUp().empty();
});




// Loading gif
var $loading = $('#loadingDiv').hide();
$(document)
  .ajaxStart(function () {
    $loading.show();
    $('#loadedDiv').hide();
  })
  .ajaxStop(function () {
    $loading.hide();
    $('#loadedDiv').show();
  });


var $loading2 = $('#loadingDiv2').hide();
$(document)
  .ajaxStart(function () {
    $loading2.show();
    $('#loadedDiv2').hide();
  })
  .ajaxStop(function () {
    $loading2.hide();
    $('#loadedDiv2').show();
  });


// $('#myModal').on('shown.bs.modal', function () {
//   $('#myInput').trigger('focus')
// })


// click character image and shrink the character image
// $(document).ready(function() {
//     $('.image-upload').click(function() {
//         $(this).animate(
//            {width: '25%', height: 'auto'}, 3000
//         );
//
//
//
//     });
// });
//
//
//


