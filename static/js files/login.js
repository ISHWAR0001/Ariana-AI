const loginbox = document.querySelector(".login-box");
const signupbox = document.querySelector(".signup-box");
const registerlink = document.querySelector(".register-link");
const login_password = document.getElementById('login-pass');
const pass_icon1 = document.getElementById('pass-icon1');

registerlink.onclick = () => {
  if (
    loginbox.classList.contains("active") &&
    signupbox.classList.contains("deactive")
  ) {
    loginbox.classList.replace("active", "deactive");
    signupbox.classList.replace("deactive", "active");
  } else {
    loginbox.classList.add("deactive");
    signupbox.classList.add("active");
  }
};

$(document).ready(function () {
  //Login button clicking events
  $("#faceAuth").click(function (e) {
    $("#login").attr("hidden", true);
    $("#start").attr("hidden", false);
    $("#Loader").attr("hidden", false);
    eel.facialRecognition()();
  });

  $("#BackBtn3").click(function (e) {
    $("#start").attr("hiddden", true);
    $("#Loader").attr("hidden", true);
    $("#login").attr("hidden", false);
    console.log("working");
    eel.exitfacialrecognition();
  });

  // Show Message
  eel.expose(showMessage);
  function showMessage(message) {
    $(".process-message li:first").text(message);
    $(".process-message").textillate("start");
  }

  // Face Authentication Animation
  //  Hide Loader and display Face Auth animation
  eel.expose(hideLoader);

  function hideLoader() {
    $("#Loader").attr("hidden", true);
    $("#FaceAuth").attr("hidden", false);
  }
  // Hide Face auth and display Face Auth success animation
  eel.expose(hideFaceAuth);

  function hideFaceAuth() {
    $("#FaceAuth").attr("hidden", true);
    $("#FaceAuthSuccess").attr("hidden", false);
  }

  // Hide success and display
  eel.expose(hideFaceAuthSuccess);

  function hideFaceAuthSuccess() {
    $("#FaceAuthSuccess").attr("hidden", true);
    $("#HelloGreet").attr("hidden", false);
  }

  // Hide Start Page and display blob
  eel.expose(hideStart);

  function hideStart() {
    $("#start").attr("hidden", true);

    setTimeout(function () {
      $("#oval").addClass("animate__animated animate__zoomIn");
    }, 1000);
    setTimeout(function () {
      $("#oval").attr("hidden", false);
    }, 1000);
  }
});

login_password.addEventListener('input', function() {
  if (login_password.value == '') {
      pass_icon1.style.display = 'inline';  // Show the eye icon
  } else {
      pass_icon1.style.display = 'none';  // Hide the eye icon
  }
});
