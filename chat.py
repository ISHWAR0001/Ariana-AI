import eel
import os 
import google.generativeai as genai

API_KEY = os.getenv("Google_Gemini_API_Key")

chatstr = ""  # Store the conversation history

# Expose this function to JavaScript so it can be called when the user sends a message
@eel.expose
def handleUserQuery(user_query):
    global chatstr
    genai.configure(api_key = API_KEY)  # Replace with your actual API key

    # Append the user message to the chat history
    chatstr += f"{user_query}\n"

    # Define the generation configuration for the AI model
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.9,
        "top_k": 50,
        "max_output_tokens": 500,
        "response_mime_type": "text/plain",
    }

    # Initialize the model
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    try:
        # Start the chat session (you can pass an empty list or previous conversation history)
        chat_session = model.start_chat(history=[])

        # Send the user's message and get the AI's response
        response = chat_session.send_message(chatstr)

        # Send the AI response back to JavaScript
        eel.handleAIResponse(response.text)

        # Append the AI's response to the chat history
        chatstr += f"{response.text}\n"

        return response.text  # Return just the response text to JavaScript
    except Exception as e:
        print(f"Error: {e}")  # Print any error that occurs
        return "Error in generating response"  # Send a fallback error message to the frontend