import google.generativeai as genai
import os
import json
import time
import sys

# Configure Google Gemini API
API_KEY = "your_google_api_key_here"  # Replace with your actual API key
genai.configure(api_key=API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")

# File to store chat history
HISTORY_FILE = os.path.expanduser("~/.gemini_chat_history.json")

# System instructions to guide the AI
SYSTEM_INSTRUCTIONS = {
    "role": "system",
    "parts": [
        "You are running in a terminal because the user used the Google Gemini API to create a text-based chatbot interface. "
        "Respond concisely, format outputs clearly, and act like a helpful AI assistant inside a command-line environment."
    ]
}

def load_history():
    """Loads chat history from a file and ensures system instructions are included."""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
                # Ensure system instructions are always present
                if history and history[0]["role"] != "system":
                    history.insert(0, SYSTEM_INSTRUCTIONS)
                return history
        except json.JSONDecodeError:
            return [SYSTEM_INSTRUCTIONS]  # Reset history if file is corrupted
    return [SYSTEM_INSTRUCTIONS]  # Start fresh with system instructions

def save_history(history):
    """Saves chat history to a file."""
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def type_effect(text, speed=0.02):
    """Simulates typing effect for output."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()  # New line after typing

def main():
    os.system("cls" if os.name == "nt" else "clear")
    print("Google Gemini Terminal\nType 'exit' to quit, 'clear' to reset history.\n")

    chat_history = load_history()

    while True:
        try:
            user_input = input("> ")
            if user_input.lower() in ["exit", "quit"]:
                save_history(chat_history)  # Save history before exiting
                break
            elif user_input.lower() == "clear":
                chat_history = [SYSTEM_INSTRUCTIONS]  # Reset history but keep system message
                save_history(chat_history)
                print("Chat history cleared (system instructions retained).")
                continue

            # Append user input to history
            chat_history.append({"role": "user", "parts": [user_input]})

            # Generate response with history
            response = model.generate_content(chat_history)
            chat_response = response.text

            # Print with typing effect
            type_effect(chat_response, speed=0.02)  # Adjust speed if needed

            # Save AI response to history
            chat_history.append({"role": "model", "parts": [chat_response]})

            # Save updated history
            save_history(chat_history)

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
