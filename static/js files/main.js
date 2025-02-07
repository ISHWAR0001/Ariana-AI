$(document).ready(function () {
  $(".text").textillate({
    loop: true,
    sync: true,
    in: {
      effect: "bounceIn",
    },
    out: {
      effect: "bounceOut",
    },
  });

  //Siri Configuration

  var siriWave = new SiriWave({
    container: document.getElementById("siri-container"),
    width: 800,
    height: 200,
    style: "ios9",
    amplitude: "1",
    speed: "0.30",
    autostart: true,
  });

  //Siri Message animation

  $(".siri-message").textillate({
    in: {
      effect: "fadeInUp",
      sync: true,
    },
    out: {
      effect: "fadeOutUp",
      sync: true,
    },
  });

  // Ensure the mic button is enabled and works on first click, even on fresh page load
  let running = false; // Track if the main function is running

  //Mic Button Click Event

  $("#MicBtn").click(function (e) {
    if (!running) {
      // Only allow starting if running is False (meaning the main function was stopped)
      $("#oval").attr("hidden", true);
      $("#SiriWave").attr("hidden", false);
      eel.ClickOnMicSound(); // Play the mic sound
      eel.run_main(); // Start the main function in a separate thread
      running = true; // Set running to true when the main function starts
    }
  });

  //display hood on clicking back button and hide siri
  $("#BackBtn1").click(function (e) {
    $("#oval").attr("hidden", false);
    $("#SiriWave").attr("hidden", true);
    // Call Python back function to stop the process
    eel.back(); // This will stop the main function in Python
    running = false; // Set running to false when the back button is clicked to stop the loop
  });

  //Chat Button Click Event
  $("#ChatBtn").click(function (e) {
    $("#oval").attr("hidden", true);
    $("#ChatBox").attr("hidden", false);
  });

  //Display Speak Message
  eel.expose(DisplayMessage);

  function DisplayMessage(message) {
    $(".siri-message li:first").text(message);
    $(".siri-message").textillate("start");
  }

  //Display Hood
  eel.expose(ShowHood);

  function ShowHood() {
    $("#oval").attr("hidden", false);
    $("#SiriWave").attr("hidden", true);
  }

  //Shortcut key or Hot Key for opening ariana directly

  function doc_KeyUp(e) {
    if (e.key === "m" && e.ctrlKey) {
      eel.ClickOnMicSound();
      $("#oval").attr("hidden", true);
      $("#SiriWave").attr("hidden", false);
      eel.main()();
    }
  }
  document.addEventListener("keyup", doc_KeyUp, false);

  function PlayAssistant(message) {
    if (message != "") {
      $("#oval").attr("hidden", true);
      $("#ChatBox").attr("hidden", false);
      eel.main(message);
      $("#chatbox1").val("");
      $("#MicBtn").attr("hidden", false);
      $("#SendBtn1").attr("hidden", true);
    }
  }

  //Make function to show send button

  function ShowHideBtn(message) {
    if (message.length == 0) {
      $("#MicBtn").attr("hidden", false);
      $("#SendBtn1").attr("hidden", true);
    } else {
      $("#MicBtn").attr("hidden", true);
      $("#SendBtn1").attr("hidden", false);
    }
  }

  $("#chatbox1").keyup(function () {
    let message = $("#chatbox1").val();
    ShowHideBtn(message);
  });

  $("#chatbox1").keydown(function (e) {
    if (e.key === "Enter") {
      e.preventDefault(); // Prevent the default behavior (e.g., form submission)

      let message = $("#chatbox1").val();
      PlayAssistant(message);
      if (message.trim() !== "") {
        // Append the message to the chat box on the right side
        const messageContainer = $(".container2"); // Assuming this is your chat container
        const newMessage = $("<div>").addClass("message right").text(message);
        messageContainer.append(newMessage);

        // Clear the input box
        $("#chatbox1").val("");
        ShowHideBtn(""); // Hide send button again and show Mic button

        // Show loading indicator
        const loadingMessage = $("<div>")
          .addClass("message left")
          .text("AI is typing...");
        messageContainer.append(loadingMessage);
        messageContainer.scrollTop(messageContainer[0].scrollHeight);

        // Auto-scroll the chat to the bottom
        messageContainer.scrollTop(messageContainer[0].scrollHeight);

        // Call Python function to handle the user query and get AI response
        eel.handleUserQuery(message)(function (response) {
          console.log("AI Response:", response); // Debug log to check AI response

          // Find and remove the loading message once the AI response is received
          $(".loading").remove();

          // Ensure response is received from Python before appending
          if (response) {
            // Create and append the assistant's response to the chat container
            const responseMessage = $("<div>")
              .addClass("message left")
              .text(response); // AI message on the left
            messageContainer.append(responseMessage);

            // Scroll to the bottom of the chat container
            messageContainer.scrollTop(messageContainer[0].scrollHeight);
          } else {
            console.log("No response from AI");
          }
        });
      }
    }
  });

  $("#SendBtn1").click(function () {
    let message = $("#chatbox1").val();
    PlayAssistant(message);
    if (message.trim() !== "") {
      // Append the message to the chat box on the right side
      const messageContainer = $(".container2"); // Assuming this is your chat container
      const newMessage = $("<div>").addClass("message right").text(message);
      messageContainer.append(newMessage);

      // Clear the input box
      $("#chatbox1").val("");
      ShowHideBtn(""); // Hide send button again and show Mic button

      // Auto-scroll the chat to the bottom
      messageContainer.scrollTop(messageContainer[0].scrollHeight);

      // Show loading indicator (AI is typing...)
      const loadingMessage = $("<div>")
        .addClass("message left loading")
        .text("AI is typing...");
      messageContainer.append(loadingMessage);
      messageContainer.scrollTop(messageContainer[0].scrollHeight);

      // Call Python function to handle the user query and get AI response
      eel.handleUserQuery(message)(function (response) {
        console.log("AI Response:", response); // Debug log to check AI response

        // Find and remove the loading message once the AI response is received
        $(".loading").remove();

        // Ensure response is received from Python before appending
        if (response) {
          // Create and append the assistant's response to the chat container
          const responseMessage = $("<div>")
            .addClass("message left")
            .text(response); // AI message on the left
          messageContainer.append(responseMessage);

          // Scroll to the bottom of the chat container
          messageContainer.scrollTop(messageContainer[0].scrollHeight);
        } else {
          console.log("No response from AI");
        }
      });
    }
    eel.handleAIResponse(message);
  });
});
