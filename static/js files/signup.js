$(document).ready(function() {
    $("#sampleface").click(function(e) {
        $("#login").attr("hidden", true);
        $("#start").attr("hidden", false);
        $("#Loader").attr("hidden", false);
        eel.takingFaceSamples()();
        eel.trainingFaceSamples()();
    });

    eel.expose(hideFaceAuth2)
    function hideFaceAuth2() {

        $("#FaceAuth").attr("hidden", true);
        $("#loadSpinner").attr("hidden", false);

    }

    eel.expose(hideloadSpinner)

    function hideloadSpinner() {

        $("#loadSpinner").attr("hidden", true);
        $("#FaceAuthSuccess").attr("hidden", false);

    }

    eel.expose(hideSampleFace)

    function hideSampleFace() {
        $("#FaceAuthSuccess").attr("hidden", true);
        $("#start").attr("hidden", true)
        $("#login").attr("hidden", false);
    }

    $(".back_btn3").click(function(e) {
        // eel.exitSampleFace()();
        $("#Loader").attr("hidden", true);
        $("#start").attr("hiddden", true);
        $("#login").attr("hidden", false);
    });
});

const loginBox = document.querySelector('.login-box');
const signupBox = document.querySelector('.signup-box')
const loginLink = document.querySelector('.login-link');
const create_password = document.getElementById('create-pass');
const confirm_password = document.getElementById('confirm-pass');
const pass_icon2 = document.getElementById('pass-icon2');
const pass_icon3 = document.getElementById('pass-icon3');

loginLink.onclick = () => {
    loginbox.classList.replace('deactive', 'active');
    signupbox.classList.replace('active', 'deactive');
}

create_password.addEventListener('input', function() {
    if (create_password.value == '') {
        pass_icon2.style.display = 'inline';  // Show the eye icon
    } else {
        pass_icon2.style.display = 'none';  // Hide the eye icon
    }
});

confirm_password.addEventListener('input', function() {
    if (confirm_password.value == '') {
        pass_icon2.style.display = 'inline';  // Show the eye icon
    } else {
        pass_icon2.style.display = 'none';  // Hide the eye icon
    }
});