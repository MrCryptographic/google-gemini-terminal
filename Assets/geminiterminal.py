import google.generativeai as genai
import os
import json
import time
import sys

# Configure Google Gemini API
API_KEY = "your_google_api_key_here"  # Replace with your actual API key
genai.configure(api_key=API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# File to store chat history
HISTORY_FILE = os.path.expanduser("~/.gemini_chat_history.json")

def load_history():
    """Loads chat history from a file."""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []  # Return empty history if the file is corrupted
    return []

def save_history(history):
    """Saves chat history to a file."""
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def type_effect(text, speed=0.03):
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
                chat_history = []  # Reset history
                save_history(chat_history)
                print("Chat history cleared.")
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
