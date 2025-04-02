# Google Gemini in the Terminal (Windows 11 Only)

<details>
  <summary>You need an API key to use this code properly</summary>
  Get it from https://aistudio.google.com/
</details>

<details>
  <summary>You also need to install Python for your version</summary>
  Go to https://python.org and install the correct version.

  Make sure to `Install in/as PATH`!

  Also after installing, open a new Powershell window and run `pip install google.generativeai` as that is required for this to work.
</details>

## Step 1 - Make the folder and create the Terminal profile.
Make a folder on your desktop called whatever you want (e.g., Google Gemini Terminal) and create a `.py` file in that folder called whatever you want (e.g., geminiterminal). Afterwards, right click on the `.py` file and click `Copy as path`, you'll need it for later.

Open Terminal by pressing `Win+X` and clicking Terminal:

![image](https://github.com/user-attachments/assets/09680f11-18eb-461c-81e7-617202e5523b)

After that, press `Ctrl+,` and click `+ Add a new profile` on the sidebar, then click `+ New Empty Profile`.
Name it anything you want, preferably `Google Gemini`.

Click on the `Command Line` dropdown. Type `py "C:\paste\your\path\here.py"` (replace that path with your copied one).
Click on `Starting Directory` and put `C:\Users\[YourUser]\Desktop`, replace [YourUser] with your user, it should be visible in the terminal (non admin) when you open Windows PowerShell.
[OPTIONAL] Make a tab title and put anything you want.

## Step 3 - Customize it!
Click Appearance at the bottom of your profile settings, and choose your font weight (boldness), Color Scheme, etc.
You can also make your own Color Scheme in the Color Scheme section in the terminal settings (if you aren't in the terminal settings already, press `Win+X` and click terminal, then press `Ctrl+,`)
![Screenshot (4)](https://github.com/user-attachments/assets/6da8954c-306e-4ed9-acec-8556e91370b2)

## Step 4 - Set up the API key for your Google Gemini.
You're probably wondering why it doesn't work yet, and that's because you need an API key (if you already have a Google Gemini API Key, skip this step):
Go to [Google AI Studio](https://aistudio.google.com) and click `🔑 Get API Key`
![Screenshot (5)](https://github.com/user-attachments/assets/27ae7603-0246-498c-b2de-2a55bebe0cca)
Copy your key and head to the folder you created in Step 1, right-click the `.py` file, click `Open with...`, and click `Notepad`.

In this empty text box, paste in the code from the [Assets](https://github.com/MrCryptographic/google-gemini-terminal/blob/main/Assets/geminiterminal.py) folder.

**Or from here:**
```python
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
```
Replace `your_google_api_key_here` with your actual api key from [Google AI Studio](https://aistudio.google.com).

[OPTIONAL] Replace `gemini-1.5-flash` with any vaild Google Gemini models, but `gemini-1.5-flash` is valid and good for fast responses. See all vaild models [here](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/models).
