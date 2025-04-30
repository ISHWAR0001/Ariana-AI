const messageInput = document.getElementById("chatbox2");
const BackBtn2 = document.getElementById("BackBtn2");
const SendBtn2 = document.getElementById("SendBtn2");

// Handle clicking back button to hide chatbox and show main panel
$("#BackBtn2").click(function (e) {
  $("#oval").attr("hidden", false);
  $("#ChatBox").attr("hidden", true);
  $(".container2").empty(); // Clear the chat container
});

// Handle sending a message when clicking 'Send' button
SendBtn2.addEventListener("click", sendMessage);

// Handle pressing Enter key to send message
messageInput.addEventListener("keypress", function (event) {
  if (event.key === "Enter") {
    sendMessage();
  }
});

// Expose this function for eel communication with Python
eel.expose(sendMessage);

function sendMessage() {
  const messageText = messageInput.value.trim();

  if (messageText) {
    const messageContainer = document.querySelector(".container2");

    // Create and append the user message to the chat container
    const newMessage = document.createElement("div");
    newMessage.classList.add("message", "right"); // User message on the right
    newMessage.innerText = messageText;
    messageContainer.appendChild(newMessage);

    // Clear the input field and focus back
    messageInput.value = "";
    messageInput.focus();

    // Scroll to the bottom to show the latest message
    messageContainer.scrollTop = messageContainer.scrollHeight;

    // Show loading indicator (AI is typing...)
    const loadingMessage = document.createElement("div");
    loadingMessage.classList.add("message", "left", "loading"); // AI loading message on the left
    loadingMessage.innerText = "AI is typing...";
    messageContainer.appendChild(loadingMessage);

    // Call Python function to handle the user query and get AI response
    eel.handleUserQuery(messageText)(function (response) {
      console.log("AI Response:", response); // Debug log to check AI response

      // Find and remove the loading message
      const loadingMessage = document.querySelector(".loading");
      if (loadingMessage) {
        loadingMessage.remove();
      }

      // Ensure response is received from Python before appending
      if (response) {
        // Create and append the assistant's response to the chat container
        const responseMessage = document.createElement("div");
        responseMessage.classList.add("message", "left"); // AI message on the left
        responseMessage.innerText = response;
        messageContainer.appendChild(responseMessage);

        // Scroll to the bottom of the chat container
        messageContainer.scrollTop = messageContainer.scrollHeight;
      } else {
        console.log("No response from AI");
      }
    });
  }
}

// Function to handle AI response from Python
eel.expose(handleAIResponse);

function handleAIResponse(responseText) {
  const messageContainer = document.querySelector(".container2");

  // Create and append the assistant's response to the chat container
  const responseMessage = document.createElement("div");
  responseMessage.classList.add("message", "left"); // AI message on the left
  responseMessage.innerText = responseText;
  messageContainer.appendChild(responseMessage);

  // Scroll to the bottom to show the latest message
  messageContainer.scrollTop = messageContainer.scrollHeight;
}
